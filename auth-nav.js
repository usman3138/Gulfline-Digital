async function updateAuthNav(){
  const enLink = document.getElementById('nav-account-en');
  const arLink = document.getElementById('nav-account-ar');
  if(!enLink || !arLink || !supabaseClient) return;

  const { data: { session } } = await supabaseClient.auth.getSession();
  if(session){
    const label = 'Sign out (' + session.user.email + ')';
    enLink.textContent = label;
    arLink.textContent = 'تسجيل الخروج (' + session.user.email + ')';
    enLink.href = '#';
    arLink.href = '#';
    const doSignOut = async (e) => {
      e.preventDefault();
      await supabaseClient.auth.signOut();
      location.reload();
    };
    enLink.onclick = doSignOut;
    arLink.onclick = doSignOut;
  }
}
updateAuthNav();
