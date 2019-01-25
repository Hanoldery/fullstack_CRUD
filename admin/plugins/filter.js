import Vue from 'vue';
import _ from 'lodash';

Vue.filter('numbers', (value) => {
  let number = value + 1
  if (number < 10) {
    return "0" + number + "."
  } 
  return number + "."
})

Vue.filter('minutes', (value) => {
  if (!value || typeof value !== "number") return "00:00"
  let min = parseInt(value / 60),
      sec = parseInt(value % 60)
  min = min < 10 ? "0" + min : min
  sec = sec < 10 ? "0" + sec : sec
  value = min + ":" + sec
  return value
})

Vue.filter('startCase', (value) => {
  return _.startCase(value);
})

Vue.filter('precision', (value) => {
  return value.toFixed(1);
})


Vue.filter('date', (value) => {
    var date = formatDate(parseDate(value));
    var d = parseDate(date);
    return d ? formatDate(d) : date;
});

// super simple pt-BR date parser
function parseDate(str) {
  if (str === null || isDate(str) || str === undefined) return str || null;
  var p = str.match(/^(\d{1,4})-(\d{1,2})-(\d{1,2})T(\d{1,2})?:(\d{1,2})?:(\d{1,2})/);
  if (!p) return null;
  return new Date(parseInt(p[1]), parseInt(p[2]) - 1, parseInt(p[3]));
}

// super simple pt-BR date format
function formatDate(dt) {
  if (dt == null) return '';
  var f = function(d) { return d < 10 ? '0' + d : d; };
  return f(dt.getDate()) + '/' + f(dt.getMonth() + 1) + '/' + dt.getFullYear();
}

// is object a date?
function isDate(d) {
    return Object.prototype.toString.call(d) === '[object Date]';
}
