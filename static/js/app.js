(() => {
  const qs=(s,c=document)=>c.querySelector(s), qsa=(s,c=document)=>[...c.querySelectorAll(s)];
  const menu=qs('[data-mobile-menu]'); qs('[data-menu-toggle]')?.addEventListener('click',()=>menu?.classList.toggle('open'));
  qsa('[data-dropdown-toggle]').forEach(btn=>btn.addEventListener('click',e=>{e.stopPropagation();qs('#'+btn.dataset.dropdownToggle)?.classList.toggle('open')}));
  document.addEventListener('click',()=>qsa('.dropdown-menu.open').forEach(x=>x.classList.remove('open')));
  qsa('[data-dismiss-toast]').forEach(btn=>btn.addEventListener('click',()=>btn.closest('.toast')?.remove()));
  setTimeout(()=>qsa('.toast').forEach(x=>x.remove()),6000);
  qsa('[data-tab]').forEach(btn=>btn.addEventListener('click',()=>{const root=btn.closest('.container,.admin-content');qsa('[data-tab]',root).forEach(b=>b.classList.remove('active'));btn.classList.add('active');qsa('[data-tab-panel]',root).forEach(p=>p.hidden=p.dataset.tabPanel!==btn.dataset.tab)}));
  const stream=qs('[data-message-stream]'); if(stream) stream.scrollTop=stream.scrollHeight;
  const messageForm=qs('[data-message-form]');
  messageForm?.addEventListener('submit',async e=>{e.preventDefault();const submit=qs('button',messageForm);submit.disabled=true;try{const res=await fetch(messageForm.action,{method:'POST',body:new FormData(messageForm),headers:{'X-Requested-With':'XMLHttpRequest'}});const data=await res.json();if(!res.ok)throw new Error(data.error||'Unable to send');if(data.ok){const row=document.createElement('div');row.className='message-row mine';row.innerHTML=`<div class="message-bubble"><p></p><small>${data.created}</small></div>`;qs('p',row).textContent=data.body;stream.appendChild(row);messageForm.reset();stream.scrollTop=stream.scrollHeight}}catch(err){alert(err.message)}finally{submit.disabled=false}});
})();
