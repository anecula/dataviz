from collections import OrderedDict, defaultdict, namedtuple
from dv.lib.http import CsvResponse, JsonResponse
from dv.models import State, ProgrammeArea


def beneficiaries_fm_gross_allocation(request):
    states = State.objects.all().only(
        'code', 'name',
        'gross_allocation_eea', 'gross_allocation_norway',
    )
    data = []
    fields = 'donor', 'beneficiary', 'amount'
    Allocation = namedtuple('Allocation', " ".join(fields))

    for state in states:
        if state.gross_allocation_norway:
            data.append(Allocation(
                "Norway", state.name, state.gross_allocation_norway
            ))
        if state.gross_allocation_eea:
            data.append(Allocation(
                "EEA", state.name, state.gross_allocation_eea
            ))

    return CsvResponse(data, fields)

def sectors_areas_allocation(request):
    """
    Returns a list of
    {
        name: "priority sector",
        children: [
            {
                name: "programme area",
                allocation: {
                    "financial mechanism": amount,
                    ...
                },
            },
            ...
        ]
    },
    ...
    """
    items = (
        ProgrammeArea.objects.select_related('priority_sector')
        .exclude(gross_allocation=0)
        .only(
            'priority_sector__type', 'priority_sector__name',
            'short_name', 'name', 'gross_allocation'
        )
        .order_by(
            'priority_sector__name', 'priority_sector__type', 'short_name'
        )
    )

    sectors = defaultdict(lambda: defaultdict(dict))

    for item in items:
        sector_name, area_name, fm, allocation = (
            item.priority_sector.name,
            item.short_name,
            str(item.priority_sector.type),
            round(item.gross_allocation),
        )

        sector = sectors[sector_name]
        area = sector[area_name]
        area[fm] = allocation

    out = tuple(
        OrderedDict((
            ("name", sector),
            ("children", tuple(
                OrderedDict((
                    ("name", area),
                    ("allocation", allocations)
                ))
                for area, allocations in areas.items()
            ))
        ))
        for sector, areas in sectors.items()
    )

    return JsonResponse(out, json_dumps_params={"indent": 2})
