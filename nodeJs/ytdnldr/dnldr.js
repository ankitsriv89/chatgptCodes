const fs = require('fs');
const ytdl = require('ytdl-core');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function downloadVideo() {
  rl.question('Enter the YouTube video URL: ', async (videoUrl) => {
    try {
      const info = await ytdl.getInfo(videoUrl);
      const videoDetails = info.videoDetails;

      console.log(`Title: ${videoDetails.title}`);
      console.log(`Author: ${videoDetails.author.name}`);
      console.log(`Length: ${videoDetails.lengthSeconds} seconds`);
      console.log(`Views: ${videoDetails.viewCount}`);
      console.log(`Description: ${videoDetails.description}`);

      const fileSize = parseInt(info.formats[0].contentLength);
      const fileSizeMB = (fileSize / (1024 * 1024)).toFixed(2);

      console.log(`File size: ${fileSizeMB} MB`);

      rl.question('Do you want to download this video? (yes/no): ', (answer) => {
        if (answer.toLowerCase() === 'yes') {
          const videoStream = ytdl(videoUrl, { quality: 'highest' });

          const outputFileName = `${videoDetails.title.replace(/[^\w\s]/gi, '')}.mp4`;
          const outputStream = fs.createWriteStream(outputFileName);

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

        } else {
          console.log('Download aborted.');
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
