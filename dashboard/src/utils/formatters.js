/**
 * Number and currency/metric formatters
 */

export const formatNumber = (num) => {
  if (num === null || num === undefined || isNaN(num)) return '0';
  const val = Number(num);
  return new Intl.NumberFormat('en-US').format(val);
};

export const formatCompact = (num) => {
  if (num === null || num === undefined || isNaN(num)) return '0';
  const val = Number(num);
  const abs = Math.abs(val);

  if (abs >= 1_000_000_000) {
    return (val / 1_000_000_000).toFixed(2).replace(/\.00$/, '') + 'B';
  }
  if (abs >= 1_000_000) {
    return (val / 1_000_000).toFixed(2).replace(/\.00$/, '') + 'M';
  }
  if (abs >= 1_000) {
    return (val / 1_000).toFixed(1).replace(/\.0$/, '') + 'K';
  }
  return val.toLocaleString('en-US');
};

export const formatPercentage = (num) => {
  if (num === null || num === undefined || isNaN(num)) return '0.00%';
  const val = Number(num);
  return val.toFixed(2) + '%';
};

export const formatHour = (hour) => {
  const h = Number(hour);
  if (h === 0) return '12 AM';
  if (h === 12) return '12 PM';
  if (h < 12) return `${h} AM`;
  return `${h - 12} PM`;
};

export const getMonthName = (monthNum) => {
  const months = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
  ];
  return months[Number(monthNum) - 1] || `Month ${monthNum}`;
};
