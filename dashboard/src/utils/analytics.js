import { getCategoryName } from '../data/categories';
import { formatHour, getMonthName } from './formatters';

const DAYS_ORDER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

/**
 * Filter data based on user filter criteria
 */
export const filterData = (data, filters) => {
  if (!data || !data.length) return [];

  const { year, channel, category, day } = filters;

  return data.filter((row) => {
    // Year filter
    if (year && year !== 'all' && Number(row.publish_year) !== Number(year)) {
      return false;
    }

    // Channel filter
    if (channel && channel !== 'all' && row.channel_title !== channel) {
      return false;
    }

    // Category filter
    if (category && category !== 'all' && Number(row.category_id) !== Number(category)) {
      return false;
    }

    // Publishing Day filter
    if (day && day !== 'all' && row.publish_day !== day) {
      return false;
    }

    return true;
  });
};

/**
 * Calculate KPI summary numbers
 */
export const calculateKPIs = (data) => {
  if (!data || !data.length) {
    return {
      totalVideos: 0,
      totalViews: 0,
      totalLikes: 0,
      totalDislikes: 0,
      totalComments: 0,
      totalEngagement: 0,
      avgEngagementRate: 0,
      avgViews: 0,
      avgLikes: 0,
      avgComments: 0,
    };
  }

  let totalViews = 0;
  let totalLikes = 0;
  let totalDislikes = 0;
  let totalComments = 0;
  let totalEngagement = 0;
  let sumEngagementRate = 0;

  for (let i = 0; i < data.length; i++) {
    const row = data[i];
    totalViews += Number(row.views) || 0;
    totalLikes += Number(row.likes) || 0;
    totalDislikes += Number(row.dislikes) || 0;
    totalComments += Number(row.comment_count) || 0;
    totalEngagement += Number(row.engagement) || 0;
    sumEngagementRate += Number(row.engagement_rate) || 0;
  }

  const count = data.length;

  return {
    totalVideos: count,
    totalViews,
    totalLikes,
    totalDislikes,
    totalComments,
    totalEngagement,
    avgEngagementRate: count > 0 ? sumEngagementRate / count : 0,
    avgViews: count > 0 ? Math.round(totalViews / count) : 0,
    avgLikes: count > 0 ? Math.round(totalLikes / count) : 0,
    avgComments: count > 0 ? Math.round(totalComments / count) : 0,
  };
};

/**
 * Views trend aggregated by trending_date
 */
export const getViewsTrend = (data) => {
  if (!data || !data.length) return [];

  const dateMap = new Map();

  for (let i = 0; i < data.length; i++) {
    const row = data[i];
    const date = row.trending_date;
    if (!date) continue;

    if (!dateMap.has(date)) {
      dateMap.set(date, {
        date,
        views: 0,
        likes: 0,
        comments: 0,
        engagementRateSum: 0,
        count: 0,
      });
    }

    const item = dateMap.get(date);
    item.views += Number(row.views) || 0;
    item.likes += Number(row.likes) || 0;
    item.comments += Number(row.comment_count) || 0;
    item.engagementRateSum += Number(row.engagement_rate) || 0;
    item.count += 1;
  }

  const result = Array.from(dateMap.values())
    .map((item) => ({
      date: item.date,
      views: item.views,
      likes: item.likes,
      comments: item.comments,
      avgEngagementRate: Number((item.engagementRateSum / item.count).toFixed(2)),
      count: item.count,
    }))
    .sort((a, b) => a.date.localeCompare(b.date));

  // If there are too many dates (e.g. 200+), downsample for smooth area chart rendering
  if (result.length > 60) {
    const step = Math.ceil(result.length / 50);
    return result.filter((_, idx) => idx % step === 0 || idx === result.length - 1);
  }

  return result;
};

/**
 * Top channels by views (Top 10)
 */
export const getTopChannelsByViews = (data, limit = 10) => {
  if (!data || !data.length) return [];

  const channelMap = new Map();

  for (let i = 0; i < data.length; i++) {
    const row = data[i];
    const ch = row.channel_title;
    if (!ch) continue;

    if (!channelMap.has(ch)) {
      channelMap.set(ch, {
        channel: ch,
        views: 0,
        likes: 0,
        comments: 0,
        videos: 0,
        engagementRateSum: 0,
      });
    }

    const item = channelMap.get(ch);
    item.views += Number(row.views) || 0;
    item.likes += Number(row.likes) || 0;
    item.comments += Number(row.comment_count) || 0;
    item.videos += 1;
    item.engagementRateSum += Number(row.engagement_rate) || 0;
  }

  return Array.from(channelMap.values())
    .map((item) => ({
      ...item,
      avgEngagementRate: Number((item.engagementRateSum / item.videos).toFixed(2)),
    }))
    .sort((a, b) => b.views - a.views)
    .slice(0, limit);
};

/**
 * Engagement breakdown by Top Categories
 */
export const getEngagementBreakdown = (data, limit = 7) => {
  if (!data || !data.length) return [];

  const catMap = new Map();

  for (let i = 0; i < data.length; i++) {
    const row = data[i];
    const catId = row.category_id;
    if (catId === undefined) continue;

    if (!catMap.has(catId)) {
      catMap.set(catId, {
        categoryId: catId,
        category: getCategoryName(catId),
        likes: 0,
        dislikes: 0,
        comments: 0,
        total: 0,
        videos: 0,
      });
    }

    const item = catMap.get(catId);
    const l = Number(row.likes) || 0;
    const d = Number(row.dislikes) || 0;
    const c = Number(row.comment_count) || 0;

    item.likes += l;
    item.dislikes += d;
    item.comments += c;
    item.total += l + d + c;
    item.videos += 1;
  }

  return Array.from(catMap.values())
    .sort((a, b) => b.total - a.total)
    .slice(0, limit);
};

/**
 * Publishing Insights: Day of Week
 */
export const getPublishingByDay = (data) => {
  const dayMap = {};
  DAYS_ORDER.forEach((d) => {
    dayMap[d] = { day: d, videos: 0, totalViews: 0, engagementRateSum: 0 };
  });

  if (data) {
    for (let i = 0; i < data.length; i++) {
      const row = data[i];
      const d = row.publish_day;
      if (dayMap[d]) {
        dayMap[d].videos += 1;
        dayMap[d].totalViews += Number(row.views) || 0;
        dayMap[d].engagementRateSum += Number(row.engagement_rate) || 0;
      }
    }
  }

  return DAYS_ORDER.map((d) => {
    const count = dayMap[d].videos;
    return {
      day: d,
      shortDay: d.slice(0, 3),
      videos: count,
      avgViews: count > 0 ? Math.round(dayMap[d].totalViews / count) : 0,
      avgEngagementRate: count > 0 ? Number((dayMap[d].engagementRateSum / count).toFixed(2)) : 0,
    };
  });
};

/**
 * Publishing Insights: Month
 */
export const getPublishingByMonth = (data) => {
  const monthMap = {};
  for (let m = 1; m <= 12; m++) {
    monthMap[m] = { monthNum: m, month: getMonthName(m), videos: 0, totalViews: 0 };
  }

  if (data) {
    for (let i = 0; i < data.length; i++) {
      const row = data[i];
      const m = Number(row.publish_month);
      if (monthMap[m]) {
        monthMap[m].videos += 1;
        monthMap[m].totalViews += Number(row.views) || 0;
      }
    }
  }

  return Object.values(monthMap).map((item) => ({
    ...item,
    avgViews: item.videos > 0 ? Math.round(item.totalViews / item.videos) : 0,
  }));
};

/**
 * Publishing Insights: Hour of Day (0 to 23)
 */
export const getPublishingByHour = (data) => {
  const hourMap = {};
  for (let h = 0; h <= 23; h++) {
    hourMap[h] = {
      hour: h,
      hourLabel: formatHour(h),
      videos: 0,
      totalViews: 0,
      engagementRateSum: 0,
    };
  }

  if (data) {
    for (let i = 0; i < data.length; i++) {
      const row = data[i];
      const h = Number(row.publish_hour);
      if (hourMap[h]) {
        hourMap[h].videos += 1;
        hourMap[h].totalViews += Number(row.views) || 0;
        hourMap[h].engagementRateSum += Number(row.engagement_rate) || 0;
      }
    }
  }

  return Object.values(hourMap).map((item) => ({
    ...item,
    avgViews: item.videos > 0 ? Math.round(item.totalViews / item.videos) : 0,
    avgEngagementRate: item.videos > 0 ? Number((item.engagementRateSum / item.videos).toFixed(2)) : 0,
  }));
};

/**
 * Channel Performance Table List (Aggregated per channel)
 */
export const getAllChannelsPerformance = (data) => {
  if (!data || !data.length) return [];

  const channelMap = new Map();

  for (let i = 0; i < data.length; i++) {
    const row = data[i];
    const ch = row.channel_title;
    if (!ch) continue;

    if (!channelMap.has(ch)) {
      channelMap.set(ch, {
        channel: ch,
        videos: 0,
        views: 0,
        likes: 0,
        comments: 0,
        dislikes: 0,
        engagementRateSum: 0,
      });
    }

    const item = channelMap.get(ch);
    item.videos += 1;
    item.views += Number(row.views) || 0;
    item.likes += Number(row.likes) || 0;
    item.comments += Number(row.comment_count) || 0;
    item.dislikes += Number(row.dislikes) || 0;
    item.engagementRateSum += Number(row.engagement_rate) || 0;
  }

  return Array.from(channelMap.values())
    .map((item) => ({
      ...item,
      avgEngagementRate: Number((item.engagementRateSum / item.videos).toFixed(2)),
    }))
    .sort((a, b) => b.views - a.views)
    .map((item, index) => ({
      rank: index + 1,
      ...item,
    }));
};

/**
 * Trending Videos Table List
 */
export const getTrendingVideos = (data, sortBy = 'views', limit = 100) => {
  if (!data || !data.length) return [];

  // Deduplicate by video_id to show unique videos, keeping max metric
  const videoMap = new Map();

  for (let i = 0; i < data.length; i++) {
    const row = data[i];
    const id = row.video_id;
    if (!id) continue;

    if (!videoMap.has(id)) {
      videoMap.set(id, {
        video_id: id,
        title: row.title,
        channel_title: row.channel_title,
        category_id: row.category_id,
        category: getCategoryName(row.category_id),
        views: Number(row.views) || 0,
        likes: Number(row.likes) || 0,
        dislikes: Number(row.dislikes) || 0,
        comment_count: Number(row.comment_count) || 0,
        engagement_rate: Number(row.engagement_rate) || 0,
        publish_time: row.publish_time,
        publish_day: row.publish_day,
      });
    } else {
      const existing = videoMap.get(id);
      // Keep highest metrics across days
      if (Number(row.views) > existing.views) {
        existing.views = Number(row.views);
        existing.likes = Number(row.likes);
        existing.dislikes = Number(row.dislikes);
        existing.comment_count = Number(row.comment_count);
        existing.engagement_rate = Number(row.engagement_rate);
      }
    }
  }

  const list = Array.from(videoMap.values());

  if (sortBy === 'likes') {
    list.sort((a, b) => b.likes - a.likes);
  } else if (sortBy === 'comments') {
    list.sort((a, b) => b.comment_count - a.comment_count);
  } else if (sortBy === 'engagement_rate') {
    list.sort((a, b) => b.engagement_rate - a.engagement_rate);
  } else {
    // Default to views
    list.sort((a, b) => b.views - a.views);
  }

  return list.slice(0, limit).map((item, index) => ({
    rank: index + 1,
    ...item,
  }));
};

/**
 * Generate dynamic key insights from filtered dataset
 */
export const getKeyInsights = (data) => {
  if (!data || !data.length) return null;

  let maxViewsVideo = data[0];
  let maxLikesVideo = data[0];
  let maxCommentsVideo = data[0];

  const channelViews = new Map();
  const channelLikes = new Map();
  const channelComments = new Map();
  const dayCounts = new Map();
  const hourCounts = new Map();

  for (let i = 0; i < data.length; i++) {
    const row = data[i];
    const views = Number(row.views) || 0;
    const likes = Number(row.likes) || 0;
    const comments = Number(row.comment_count) || 0;
    const ch = row.channel_title;
    const day = row.publish_day;
    const hour = row.publish_hour;

    // Videos
    if (views > (Number(maxViewsVideo.views) || 0)) maxViewsVideo = row;
    if (likes > (Number(maxLikesVideo.likes) || 0)) maxLikesVideo = row;
    if (comments > (Number(maxCommentsVideo.comment_count) || 0)) maxCommentsVideo = row;

    // Channels
    if (ch) {
      channelViews.set(ch, (channelViews.get(ch) || 0) + views);
      channelLikes.set(ch, (channelLikes.get(ch) || 0) + likes);
      channelComments.set(ch, (channelComments.get(ch) || 0) + comments);
    }

    // Days
    if (day) {
      dayCounts.set(day, (dayCounts.get(day) || 0) + 1);
    }

    // Hours
    if (hour !== undefined) {
      hourCounts.set(hour, (hourCounts.get(hour) || 0) + 1);
    }
  }

  // Find max channel views
  let topChannelViews = { name: 'N/A', value: 0 };
  for (const [name, val] of channelViews.entries()) {
    if (val > topChannelViews.value) topChannelViews = { name, value: val };
  }

  // Find max channel likes
  let topChannelLikes = { name: 'N/A', value: 0 };
  for (const [name, val] of channelLikes.entries()) {
    if (val > topChannelLikes.value) topChannelLikes = { name, value: val };
  }

  // Find max channel comments
  let topChannelComments = { name: 'N/A', value: 0 };
  for (const [name, val] of channelComments.entries()) {
    if (val > topChannelComments.value) topChannelComments = { name, value: val };
  }

  // Peak day
  let peakDay = { day: 'N/A', count: 0 };
  for (const [d, count] of dayCounts.entries()) {
    if (count > peakDay.count) peakDay = { day: d, count };
  }

  // Peak hour
  let peakHour = { hour: 0, count: 0 };
  for (const [h, count] of hourCounts.entries()) {
    if (count > peakHour.count) peakHour = { hour: h, count };
  }

  return {
    topChannelViews,
    topChannelLikes,
    topChannelComments,
    maxViewsVideo: {
      title: maxViewsVideo.title,
      channel: maxViewsVideo.channel_title,
      views: Number(maxViewsVideo.views) || 0,
    },
    maxLikesVideo: {
      title: maxLikesVideo.title,
      channel: maxLikesVideo.channel_title,
      likes: Number(maxLikesVideo.likes) || 0,
    },
    maxCommentsVideo: {
      title: maxCommentsVideo.title,
      channel: maxCommentsVideo.channel_title,
      comments: Number(maxCommentsVideo.comment_count) || 0,
    },
    peakDay,
    peakHour: {
      hour: peakHour.hour,
      label: formatHour(peakHour.hour),
      count: peakHour.count,
    },
  };
};

/**
 * Extract filter options (years, categories, top channels, days)
 */
export const getFilterOptions = (data) => {
  if (!data || !data.length) {
    return { years: [], channels: [], categories: [], days: DAYS_ORDER };
  }

  const yearsSet = new Set();
  const categorySet = new Set();
  const channelFreq = new Map();

  for (let i = 0; i < data.length; i++) {
    const row = data[i];
    if (row.publish_year) yearsSet.add(row.publish_year);
    if (row.category_id) categorySet.add(row.category_id);
    if (row.channel_title) {
      channelFreq.set(row.channel_title, (channelFreq.get(row.channel_title) || 0) + 1);
    }
  }

  const sortedYears = Array.from(yearsSet).sort((a, b) => b - a);
  const sortedCategories = Array.from(categorySet)
    .map((id) => ({ id, name: getCategoryName(id) }))
    .sort((a, b) => a.name.localeCompare(b.name));

  // Top 50 channels by video frequency for the dropdown selector
  const sortedChannels = Array.from(channelFreq.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 50)
    .map(([name]) => name)
    .sort();

  return {
    years: sortedYears,
    channels: sortedChannels,
    categories: sortedCategories,
    days: DAYS_ORDER,
  };
};
