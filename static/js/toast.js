const toaster = document.getElementById('toaster');

const newToast = (text, category) => {
    let toast = createToast(text, category)
    addToast(toast)
  
    return new Promise(async (resolve, reject) => {
      await Promise.allSettled(
        toast.getAnimations().map(animation => 
          animation.finished
        )
      )
      toaster.removeChild(toast)
      resolve() 
    })
  }

const createToast = (text, category) => {
    const toast = document.createElement('output');

    toast.innerText = text;
    toast.classList.add('gui-toast');
    toast.setAttribute('role', 'status');

    if (category) {
        toast.classList.add(`gui-toast-${category}`);
    }

    return toast;
}

const addToast = (toast) => {
    const { matches:motionOK } = window.matchMedia(
      '(prefers-reduced-motion: no-preference)'
    )

    console.log(toaster)
  
    toaster.children.length && motionOK
      ? flipToast(toast)
      : toaster.appendChild(toast)
  }

const flipToast = toast => {
  // FIRST
  const first = toaster.offsetHeight

  // add new child to change container size
  toaster.appendChild(toast)

  // LAST
  const last = toaster.offsetHeight

  // INVERT
  const invert = last - first

  // PLAY
  const animation = toaster.animate([
    { transform: `translateY(${invert}px)` },
    { transform: 'translateY(0)' }
  ], {
    duration: 150,
    easing: 'ease-out',
  })
}