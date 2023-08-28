const fs = require('fs');
const ytdl = require('ytdl-core');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function formatBytes(bytes) {
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  if (bytes === 0) return '0 Byte';
  const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
  //const fileSizeMB = parseInt(bytes / (1024 * 1024)).toFixed(2);

  return `${Math.round(bytes / Math.pow(1024, i), 2).toFixed(2)}`;
  return fileSizeMB;
}

function downloadVideo() {
  rl.question('Enter the YouTube video URL: ', async (videoUrl) => {
    try {
      const info = await ytdl.getInfo(videoUrl);
      const videoDetails = info.videoDetails;

      console.log(`Title: ${videoDetails.title}`);
      console.log(`Author: ${videoDetails.author.name}`);
      console.log(`Length: ${(videoDetails.lengthSeconds/60).toFixed(2)} minutes`);
      //console.log(`Views: ${videoDetails.viewCount}`);
      console.log(`Description: ${videoDetails.description}`);

      const formats = ytdl.filterFormats(info.formats, 'videoandaudio');

      console.log('Available video quality options:');
      formats.forEach((format, index) => {
        console.log(`[${index + 1}] ${format.qualityLabel} - ${format.container}`);
        console.log(`    File Size: ${formatBytes(format.contentLength)}`);
      });

      rl.question('Select the desired quality (enter the corresponding number): ', (answer) => {
        const selectedFormat = formats[parseInt(answer) - 1];
        if (selectedFormat) {
          rl.question('Enter download location (e.g., /path/to/directory/): ', (downloadLocation) => {
          downloadLocation = downloadLocation.trim(); // Remove leading/trailing spaces

          const videoStream = ytdl(videoUrl, { format: selectedFormat });

          const outputFileName = `${videoDetails.title.replace(/[^\w\s]/gi, '')}_${selectedFormat.qualityLabel}.${selectedFormat.container}`;
          const outputPath = `${downloadLocation}/${outputFileName}`;

          const outputStream = fs.createWriteStream(outputPath);

          videoStream.pipe(outputStream);

          videoStream.on('progress', (chunkLength, downloaded, total) => {
            const progress = (downloaded / total) * 100;
            process.stdout.clearLine();
            process.stdout.cursorTo(0);
            process.stdout.write(`Downloaded: ${progress.toFixed(2)}%`);
          });

          outputStream.on('finish', () => {
            console.log('\nDownload completed.');
            rl.close();
          });
        });

        } else {
          console.log('Invalid selection.');
          rl.close();
        }
      });
    } catch (error) {
      console.error('Error:', error.message);
      rl.close();
    }
  });
}

downloadVideo();
