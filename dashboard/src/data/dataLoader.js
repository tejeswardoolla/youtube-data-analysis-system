import Papa from 'papaparse';

let cachedData = null;

export const loadYouTubeData = async (onProgress) => {
  if (cachedData) {
    return cachedData;
  }

  try {
    if (onProgress) onProgress(20, 'Fetching dataset file...');
    
    // Attempt to load from public folder
    const response = await fetch('/youtube_dashboard_data.csv');
    if (!response.ok) {
      throw new Error(`Failed to fetch CSV: ${response.statusText}`);
    }

    if (onProgress) onProgress(50, 'Parsing 33,089 YouTube records...');
    const csvText = await response.text();

    return new Promise((resolve, reject) => {
      Papa.parse(csvText, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
        worker: false,
        complete: (results) => {
          if (onProgress) onProgress(90, 'Structuring analytics...');

          // Filter out any broken empty rows if any
          const cleanData = results.data.filter(
            (row) => row.video_id && row.views !== undefined && !isNaN(row.views)
          );

          cachedData = cleanData;
          if (onProgress) onProgress(100, 'Ready');
          resolve(cleanData);
        },
        error: (error) => {
          reject(error);
        }
      });
    });
  } catch (error) {
    console.error('Error loading YouTube data:', error);
    throw error;
  }
};
