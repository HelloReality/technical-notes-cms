// Generate the Instagram carousel HTML note (notebook aesthetic matching
// the existing Linux Security Handbook note) with all 20 images.
import { writeFileSync } from "fs";

const ASSETS = "/uploads/instagram-carousel-DcdSiAhFbh0";
const PAGES = 20;

const images = Array.from({ length: PAGES }, (_, i) => {
  const n = String(i + 1).padStart(2, "0");
  return {
    num: n,
    src: `${ASSETS}/page-${n}.jpg`,
    alt: `Instagram carousel page ${i + 1} of ${PAGES}`,
  };
});

const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Instagram Carousel — 20 Pages</title>
<style>
  /* ============================================================
     RESET & ROOT VARIABLES
     ============================================================ */
  :root{
    --paper:#f5f1e8;
    --paper-2:#efe9dd;
    --grid-line:#bcc8d6;
    --navy:#15264d;
    --navy-2:#1e3160;
    --ink:#1c1c1c;
    --ink-2:#3a3f47;
    --blue:#2563eb;
    --blue-soft:#cfe0ff;
    --green:#16a34a;
    --green-soft:#cdf3da;
    --purple:#7c3aed;
    --purple-soft:#e2d4ff;
    --red:#dc2626;
    --red-soft:#ffd4d4;
    --gold:#d4a017;
    --gold-soft:#fce9b6;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html,body{background:#cfc9bb;}
  body{
    font-family:"Inter","Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    -webkit-font-smoothing:antialiased;
    color:var(--ink);
    display:flex;flex-direction:column;align-items:center;gap:32px;
    padding:24px 12px;
  }

  /* Wrapper holds page + binding, allows ring to extend outside page */
  .page-wrapper{
    position:relative;
    width:1080px;
  }

  /* ============================================================
     PAGE / NOTEBOOK SHEET
     ============================================================ */
  .page{
    position:relative;
    width:1080px;
    background:var(--paper);
    border-radius:14px;
    box-shadow:0 22px 60px rgba(0,0,0,0.28), 0 2px 0 rgba(0,0,0,0.06) inset;
    overflow:hidden;
    padding:42px 50px 26px 78px;
  }

  /* Graph paper grid */
  .page::before{
    content:"";
    position:absolute;inset:0;
    background-image:
      linear-gradient(to right, var(--grid-line) 1px, transparent 1px),
      linear-gradient(to bottom, var(--grid-line) 1px, transparent 1px);
    background-size:26px 26px;
    opacity:.5;
    pointer-events:none;
    z-index:0;
  }

  /* ============================================================
     SPIRAL BINDING (left edge, extends outside page)
     ============================================================ */
  .spiral{
    position:absolute;
    z-index:7;
    top:0;
    left:-30px;
    width:120px;
    height:100%;
    pointer-events:none;
    background-image: url("data:image/svg+xml;utf8,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20width='90'%20height='70'%20viewBox='0%200%2090%2070'%20fill='none'%3E%3Cpath%20d='M32%2027%20C20%2028%2010%2032%2010%2035%20C10%2040%2019%2043%2032%2044%20C52%2045%2070%2042%2082%2038'%20stroke='%23111'%20stroke-width='3'%20stroke-linecap='round'%20stroke-linejoin='round'/%3E%3Cpath%20d='M32%2034%20C20%2035%2010%2039%2010%2042%20C10%2047%2019%2050%2032%2051%20C52%2052%2070%2049%2082%2045'%20stroke='%23111'%20stroke-width='3'%20stroke-linecap='round'%20stroke-linejoin='round'/%3E%3C/svg%3E");
    background-repeat:repeat-y;
    background-position:0 0;
  }
  /* Punch holes */
  .holes{
    position:absolute;
    z-index:6;
    top:0;
    left:18px;
    width:24px;
    height:100%;
    pointer-events:none;
    background-image: radial-gradient(circle, #c9bfa8 3px, transparent 4px);
    background-size:24px 80px;
    background-position:center 40px;
    background-repeat:repeat-y;
  }

  /* ============================================================
     HEADER (badges)
     ============================================================ */
  header{
    position:relative;
    z-index:2;
    display:flex;
    justify-content:flex-end;
    gap:12px;
    margin-bottom:24px;
  }
  .badge{
    background:var(--navy);
    color:#fff;
    padding:8px 18px;
    border-radius:999px;
    font-size:11px;
    font-weight:700;
    letter-spacing:.5px;
    text-transform:uppercase;
  }
  .badge.alt{background:var(--navy-2);}

  /* ============================================================
     TITLE
     ============================================================ */
  .title-wrap{position:relative;z-index:2;margin-bottom:28px;}
  h1{
    font-size:2.4rem;
    line-height:1.1;
    color:var(--navy);
    text-transform:uppercase;
    font-weight:800;
    letter-spacing:-.5px;
    margin-bottom:10px;
  }
  .title-underline{
    height:2px;
    background:var(--navy);
    width:100%;
    position:relative;
    display:flex;align-items:center;justify-content:center;
  }
  .title-underline::after{
    content:"";
    width:10px;height:10px;
    background:var(--navy);
    border-radius:50%;
    position:absolute;
    left:50%;
    transform:translateX(-50%);
    top:-4px;
  }

  /* ============================================================
     IMAGE GRID
     ============================================================ */
  .images{
    position:relative;
    z-index:2;
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:24px;
  }
  .figure{
    position:relative;
    border-radius:12px;
    overflow:hidden;
    background:#fff;
    box-shadow:0 4px 14px rgba(0,0,0,0.1);
  }
  .figure img{
    display:block;
    width:100%;
    height:auto;
  }
  .figure .caption{
    background:var(--navy);
    color:#fff;
    padding:8px 14px;
    font-size:11px;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:.5px;
    display:flex;
    justify-content:space-between;
    align-items:center;
  }
  .figure .caption .pg{
    background:var(--gold);
    color:var(--navy);
    border-radius:999px;
    padding:2px 10px;
    font-size:10px;
  }

  /* ============================================================
     FOOTER
     ============================================================ */
  footer{
    position:relative;
    z-index:2;
    margin-top:28px;
    padding-top:16px;
    border-top:2px dashed var(--grid-line);
    display:flex;
    justify-content:space-between;
    align-items:center;
    font-size:11px;
    color:var(--ink-2);
  }
  footer .src{
    background:var(--green-soft);
    color:var(--green);
    padding:6px 14px;
    border-radius:999px;
    font-weight:600;
  }
</style>
</head>
<body>

${images
  .map(
    (img, i) => `
  <div class="page-wrapper">
    <div class="spiral" aria-hidden="true"></div>
    <div class="holes" aria-hidden="true"></div>
    <section class="page">
      <header>
        <span class="badge">Instagram Carousel</span>
        <span class="badge alt">Page ${i + 1} of ${PAGES}</span>
      </header>
      <div class="title-wrap">
        <h1>Carousel Page ${String(i + 1).padStart(2, "0")}</h1>
        <div class="title-underline"></div>
      </div>
      <div class="images">
        <figure class="figure">
          <img src="${img.src}" alt="${img.alt}" loading="lazy" />
          <figcaption class="caption">
            <span>Carousel Image</span>
            <span class="pg">${img.num} / ${PAGES}</span>
          </figcaption>
        </figure>
      </div>
      <footer>
        <span>Imported from Instagram post DcdSiAhFbh0</span>
        <span class="src">instagram.com</span>
      </footer>
    </section>
  </div>`,
  )
  .join("")}

</body>
</html>
`;

writeFileSync("public/uploads/instagram-carousel-dcdsiahfbh0.html", html);
console.log(
  `Generated public/uploads/instagram-carousel-dcdsiahfbh0.html with ${PAGES} image pages`,
);
