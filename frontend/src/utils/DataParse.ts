import moment from "moment";

export default {
  UTCToLocal: (date: string, format: string = "DD/MM/YYYY HH:mm") => {
    return moment.utc(date).local().format(format);
  },
};
