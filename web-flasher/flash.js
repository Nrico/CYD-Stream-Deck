const connectBtn = document.getElementById('connect');
const flashBtn = document.getElementById('flash');
const copyBtn = document.getElementById('copy');
const logEl = document.getElementById('log');

let esptool;

function log(msg) {
  logEl.textContent += msg + '\n';
}

connectBtn.addEventListener('click', async () => {
  try {
    esptool = new ESPLoader();
    await esptool.connect();
    await esptool.flush();
    log('Connected to serial port');
    flashBtn.disabled = false;
  } catch (err) {
    log('Connection failed: ' + err);
  }
});

flashBtn.addEventListener('click', async () => {
  flashBtn.disabled = true;
  log('Fetching firmware...');
  try {
    // fetch firmware binary placed next to this file
    const resp = await fetch('firmware.uf2');
    const fwData = new Uint8Array(await resp.arrayBuffer());
    await esptool.writeFlash([[0x0, fwData]]);
    log('Flashing complete, resetting...');
    await esptool.hardReset();
    await esptool.disconnect();
    log('Waiting for CIRCUITPY drive to mount...');
    // Give user time to select the drive
    setTimeout(() => copyBtn.disabled = false, 4000);
  } catch (err) {
    log('Flash failed: ' + err);
  }
});

copyBtn.addEventListener('click', async () => {
  copyBtn.disabled = true;
  try {
    const rootDir = await window.showDirectoryPicker({ id: 'circuitpy' });
    log('Copying main.py');
    const mainResp = await fetch('../main.py');
    const fileHandle = await rootDir.getFileHandle('main.py', { create: true });
    const writable = await fileHandle.createWritable();
    await writable.write(await mainResp.arrayBuffer());
    await writable.close();

    log('Ensuring lib folder exists');
    const libDir = await rootDir.getDirectoryHandle('lib', { create: true });

    const libs = ['adafruit_display_shapes', 'adafruit_display_text', 'adafruit_touchscreen', 'adafruit_hid'];
    for (const lib of libs) {
      try {
        const resp = await fetch(`libs/${lib}.zip`);
        if (!resp.ok) continue;
        const data = await resp.arrayBuffer();
        const zip = await JSZip.loadAsync(data);
        const libFolder = await libDir.getDirectoryHandle(lib, { create: true });
        for (const [name, file] of Object.entries(zip.files)) {
          if (file.dir) continue;
          const fHandle = await libFolder.getFileHandle(name, { create: true });
          const wr = await fHandle.createWritable();
          await wr.write(await file.async('arraybuffer'));
          await wr.close();
        }
        log(`Copied ${lib}`);
      } catch (e) {
        log(`Skipping ${lib}: ${e}`);
      }
    }
    log('Copy complete!');
  } catch (err) {
    log('Copy failed: ' + err);
  }
});
