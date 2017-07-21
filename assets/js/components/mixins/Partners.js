export default {
  data() {
    return {
    };
  },

  created() {
    this.filter_by.push('donor_state');
    for (const col of this.aggregate_on) {
      // remove the filtering
      if (typeof col == "object")
        delete col.filter_by;
    }
  },
};
