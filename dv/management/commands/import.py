import logging
import pyexcel
import os.path
from functools import partial
from itertools import cycle

from django.core.management.base import BaseCommand, CommandError
from django.core.cache import cache
from django.db import IntegrityError
from django.conf import settings

from dv.models import (
    FinancialMechanism, State, PrioritySector, ProgrammeArea,
    Allocation,
    Programme, Programme_ProgrammeArea,
    Outcome, ProgrammeOutcome, Indicator, ProgrammeIndicator,
    Project, ProjectTheme,
    Organisation, OrganisationRole, Organisation_OrganisationRole
)
from dv.lib.utils import is_iter

logger = logging.getLogger('dv.import')

EXCEL_FILES = (
    'BeneficiaryState',
    'BeneficiaryStatePrioritySector',
    'Programme',
    'ProgrammeOutcome',
    'ProgrammeIndicators',
    'Project',
    'ProjectThemes',
    'Organisation',
    'OrganisationRoles',
)

MODELS = (
    State,
    FinancialMechanism,
    PrioritySector,
    ProgrammeArea,
    Allocation,
    Programme,
    Programme_ProgrammeArea,
    Outcome,
    ProgrammeOutcome,
    Indicator,
    ProgrammeIndicator,
    Project,
    ProjectTheme,
    Organisation,
    OrganisationRole,
    Organisation_OrganisationRole,
)
#MODELS = (PrioritySector,Allocation,)
#EXCEL_FILES = ('BeneficiaryStatePrioritySector',)


class Command(BaseCommand):
    help = 'Import the files in the directory given as argument'

    def add_arguments(self, parser):
        parser.add_argument('directory',
                            help="a directory containing spreadsheet files. xlsx is supported")

    def handle(self, *args, **options):
        directory_path = options['directory']
        if not os.path.exists(directory_path):
            raise CommandError('Cannot open directory "%s".' % directory_path)

        files = [
            f for f in os.listdir(directory_path)
            if (
                os.path.isfile(os.path.join(directory_path, f)) and
                f.endswith('.xlsx') and
                f[:-5] in EXCEL_FILES
            )
        ]
        if not files:
            raise CommandError('Directory %s is empty' % directory_path)

        existing_books = [file.split('.')[0] for file in files]
        for file in EXCEL_FILES:
            if file not in existing_books:
                raise CommandError('%s workbook is missing' % file)

        def _write(*args, **kwargs):
            self.stderr.write(*args, **kwargs)
            self.stderr.flush()
        _inline = partial(_write, ending='')
        _back = chr(8)
        throbber = cycle(_back + c for c in r'\|/-')
        self.stderr.style_func = None

        sheets = dict()

        for file in files:
            _write('Loading %s\n' % (file))
            file_path = os.path.join(directory_path, file)
            book = pyexcel.get_book(file_name=file_path)
            name = file.split('.')[0]
            sheets[name] = book[name]

        for sheet in sheets.values():
            sheet.name_columns_by_row(0)

        def _convert_nulls(record):
            for k, v in record.items():
                if v in ('NULL', 'None', ''):
                    record[k] = None
                elif hasattr(record[k], 'strip'):
                    record[k] = record[k].strip()

        for model in MODELS:
            for idx, import_src in enumerate(model.IMPORT_SOURCES):
                sheet_name = import_src['src']
                sheet = sheets[sheet_name]

                _write('Importing "%s" into %s …  ' % (sheet_name, model._meta.label))

                pk_cache = set()

                rows = updated = failed = skipped = 0

                def _save(obj):
                    nonlocal updated, failed, pk_cache
                    if (obj.pk and obj.pk in pk_cache):
                        return
                    try:
                        obj.save()
                        pk_cache.add(obj.pk)
                        updated += 1
                    except IntegrityError as e:
                        failed += 1
                        raise
                        # NOTE This is backend specific; might change on switch, say, postgres

                for record in sheet.records:
                    rows += 1
                    if settings.DEBUG:
                        _inline(next(throbber))
                    _convert_nulls(record)

                    obj = model.from_data(record, idx)
                    if obj is None:
                        # trust the class, it knows why it refused object creation
                        skipped += 1
                        continue

                    if is_iter(obj):
                        for _obj in obj:
                            _save(_obj)
                    else:
                        _save(obj)

                _write(_back + "Imported %s (%d rows): %d updated, %d skipped, %d failed" % (
                    model._meta.label, rows, updated, skipped, failed
                ), self.style.SUCCESS)

        cache.clear()
        _write("Cache cleared")
