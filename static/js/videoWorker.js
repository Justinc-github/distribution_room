self.onmessage = function(e) {
  const {data} = e;
  const blob = new Blob([data], {type: 'image/jpeg'});
  const img = new Image();
  img.onload = function() {
    const canvas = document.createElement('canvas');
    canvas.width = img.width;
    canvas.height = img.height;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);
    const frame = canvas.toDataURL('image/jpeg');
    postMessage({frame, width: img.width, height: img.height});
  };
  img.src = URL.createObjectURL(blob);
};