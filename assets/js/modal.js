export function initModal(modal){
  const closeBtn = modal.querySelector('[data-close]');
  const overlay = modal.querySelector('.overlay');
  const focusable = () => Array.from(modal.querySelectorAll('button, [href], input, textarea, select, [tabindex]:not([tabindex="-1"])'));
  function open(){
    modal.hidden = false; modal.setAttribute('aria-hidden','false');
    const first = focusable()[0]; if(first) first.focus();
  }
  function close(){ modal.hidden = true; modal.setAttribute('aria-hidden','true'); }
  modal.addEventListener('keydown', e=>{
    if(e.key==='Escape') close();
    if(e.key==='Tab'){
      const f = focusable(); if(!f.length) return;
      const i = f.indexOf(document.activeElement);
      if(e.shiftKey && i===0){ f[f.length-1].focus(); e.preventDefault(); }
      else if(!e.shiftKey && i===f.length-1){ f[0].focus(); e.preventDefault(); }
    }
  });
  overlay?.addEventListener('click', close);
  closeBtn?.addEventListener('click', close);
  return {open, close};
}
