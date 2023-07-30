let pdfDoc = null;
let pageNum = 1;
let pageRendering = false;
let pageNumPending = null;
let scale = 1.0;
let rotate = 0;
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
const pdfContainer = document.getElementById('pdf-container');
const prevPageBtn = document.getElementById('prev-page-btn');
const nextPageBtn = document.getElementById('next-page-btn');
const zoomInBtn = document.getElementById('zoom-in-btn');
const zoomOutBtn = document.getElementById('zoom-out-btn');
const rotateBtn = document.getElementById('rotate-btn');

// 初始化PDF.js
pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.8.335/pdf.worker.min.js';

// 加载PDF文档
const loadPdf = (url) => {
  pdfjsLib.getDocument(url).promise.then((pdfDoc_) => {
    pdfDoc = pdfDoc_;
    renderPage(pageNum);
  }).catch((err) => {
    console.error(err);
  });
};

// 渲染PDF页面
const renderPage = (num) => {
  pageRendering = true;
  pdfDoc.getPage(num).then((page) => {
    const viewport = page.getViewport({ scale, rotation: rotate });
    canvas.height = viewport.height;
    canvas.width = viewport.width;
    const renderContext = {
      canvasContext: ctx,
      viewport,
    };
    page.render(renderContext).promise.then(() => {
      pageRendering = false;
      if (pageNumPending !== null) {
        renderPage(pageNumPending);
        pageNumPending = null;
      }
    });
  });
  // 更新页面信息
  document.getElementById('page-num').textContent = num;
  document.getElementById('page-count').textContent = pdfDoc.numPages;
  // 更新按钮状态
  prevPageBtn.disabled = num <= 1;
  nextPageBtn.disabled = num >= pdfDoc.numPages;
  zoomInBtn.disabled = scale >= 2.0;
  zoomOutBtn.disabled = scale <= 0.5;
  rotateBtn.disabled = false;
};

// 上一页
const prevPage = () => {
  if (pageNum <= 1) {
    return;
  }
  pageNum--;
  renderPage(pageNum);
};

// 下一页
const nextPage = () => {
  if (pageNum >= pdfDoc.numPages) {
    return;
  }
  pageNum++;
  renderPage(pageNum);
};

// 放大
const zoomIn = () => {
  if (scale >= 2.0) {
    return;
  }
  scale += 0.1;
  renderPage(pageNum);
};

// 缩小
const zoomOut = () => {
  if (scale <= 0.5) {
    return;
  }
  scale -= 0.1;
  renderPage(pageNum);
};

// 旋转
const rotatePage = () => {
  rotate = (rotate + 90) % 360;
  renderPage(pageNum);
};

// 监听文件选择
document.getElementById('file-input').addEventListener('change', (evt) => {
  const file = evt.target.files[0];
  if (file.type !== 'application/pdf') {
    console.error('选择的文件不是PDF格式');
    return;
  }
  const fileReader = new FileReader();
  fileReader.onload = () => {
    const url = fileReader.result;
    loadPdf(url);
  };
  fileReader.readAsDataURL(file);
});

// 监听按钮点击
prevPageBtn.addEventListener('click', prevPage);
nextPageBtn.addEventListener('click', nextPage);
zoomInBtn.addEventListener('click', zoomIn);
zoomOutBtn.addEventListener('click', zoomOut);
rotateBtn.addEventListener('click', rotatePage);