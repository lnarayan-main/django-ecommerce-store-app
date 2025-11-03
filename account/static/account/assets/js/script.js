/* cart */
// document.addEventListener('DOMContentLoaded', function () {
//   const cartIcon = document.querySelector('.cart-wrapper');
//   const cartDropdown = cartIcon.querySelector('.group-hover\\:block');

//   cartIcon.addEventListener('mouseenter', function () {
//       clearTimeout(cartIcon.__timer);
//       cartDropdown.classList.remove('hidden');
//   });

//   cartIcon.addEventListener('mouseleave', function () {
//       cartIcon.__timer = setTimeout(() => {
//           cartDropdown.classList.add('hidden');
//       }, 1300);
//   });

//   cartDropdown.addEventListener('mouseenter', function () {
//       clearTimeout(cartIcon.__timer);
//   });

//   cartDropdown.addEventListener('mouseleave', function () {
//       cartIcon.__timer = setTimeout(() => {
//           cartDropdown.classList.add('hidden');
//       }, 1300);
//   });
// });

/* mobile menu */
document.addEventListener("DOMContentLoaded", function () {
  const hamburgerBtn = document.getElementById('hamburger');
  const mobileMenu = document.querySelector('.mobile-menu');

  hamburgerBtn.addEventListener('click', function () {
    mobileMenu.classList.toggle('hidden');
  });
});

/* swiper slider */
if (typeof Swiper !== 'undefined') {
  var swiper = new Swiper('.swiper', {
    slidesPerView: 2,
    loop: true,
    autoplay: {
        delay: 3000,
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    breakpoints: {
        1024: {
            slidesPerView: 5,
        },
    },
  });

  var swiper = new Swiper('.main-slider', {
    slidesPerView: 1,
    loop: true,
    autoplay: {
      delay: 5000,
  },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
  });
}

/* search icon show/hide */
document.getElementById('search-icon').addEventListener('click', function() {
  var searchField = document.getElementById('search-field');
  if (searchField.classList.contains('hidden')) {
      searchField.classList.remove('hidden');
      searchField.classList.add('search-slide-down');
  } else {
      searchField.classList.add('hidden');
      searchField.classList.remove('search-slide-down');
  }
});

function toggleDropdown(id, show) {
  const dropdown = document.getElementById(id);
  if (show) {
      dropdown.classList.remove('hidden');
  } else {
      dropdown.classList.add('hidden');
  }
}

function changeImage(element) {
  var mainImage = document.getElementById('main-image');
  mainImage.src = element.getAttribute('data-full');
}

/* single page product count */
document.addEventListener('DOMContentLoaded', function () {
    const decreaseButton = document.getElementById('decrease');
    const increaseButton = document.getElementById('increase');
    const quantityInput = document.getElementById('quantity');
    const productPriceElement = document.getElementById('product-price');
    const addToCartButton = document.getElementById('add-to-cart-btn');
  
    if (decreaseButton && increaseButton && quantityInput) {
        decreaseButton.addEventListener('click', function () {
            let quantity = parseInt(quantityInput.value);
            if (quantity > 1) {
                quantity -= 1;
                quantityInput.value = quantity;
            }
            updateButtons();
            let productPrice = decreaseButton.dataset.price;
            productPriceElement.textContent = '$'+(quantity * productPrice).toFixed(2);
            addToCartButton.dataset.quantity = quantity;
        });
  
        increaseButton.addEventListener('click', function () {
            let quantity = parseInt(quantityInput.value);
            quantity += 1;
            quantityInput.value = quantity;
            updateButtons();
            let productPrice = increaseButton.dataset.price;
            productPriceElement.textContent = '$'+(quantity * productPrice).toFixed(2);
            addToCartButton.dataset.quantity = quantity;
        });
  
        function updateButtons() {
            if (parseInt(quantityInput.value) === 1) {
                decreaseButton.setAttribute('disabled', true);
            } else {
                decreaseButton.removeAttribute('disabled');
            }
        }
    }
  });

/* single product tabs */
document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.tab');
    const contents = document.querySelectorAll('.tab-content');

    if (tabs.length > 0 && contents.length > 0) {
        tabs.forEach(tab => {
            tab.addEventListener('click', function () {
                tabs.forEach(t => {
                    t.classList.remove('active');
                    t.setAttribute('aria-selected', 'false');
                });
                contents.forEach(c => c.classList.add('hidden'));

                this.classList.add('active');
                this.setAttribute('aria-selected', 'true');
                document.querySelector(`#${this.id.replace('-tab', '-content')}`).classList.remove('hidden');
            });
        });

        tabs[0].click();
    }
});


/* shop page filter show/hide */
document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('products-toggle-filters');
    const filters = document.getElementById('filters');

    if (toggleButton && filters) {
        toggleButton.addEventListener('click', function() {
            if (filters.classList.contains('hidden')) {
                filters.classList.remove('hidden');
                this.textContent = 'Hide Filters';
            } else {
                filters.classList.add('hidden');
                this.textContent = 'Show Filters';
            }
        });
    }
});

/* shop page filter*/
document.addEventListener('DOMContentLoaded', function () {
    const selectElement = document.querySelector('select');
    const arrowDown = document.getElementById('arrow-down');
    const arrowUp = document.getElementById('arrow-up');

    if (selectElement && arrowDown && arrowUp) {
        selectElement.addEventListener('click', function () {
            arrowDown.classList.toggle('hidden');
            arrowUp.classList.toggle('hidden');
        });
    }
});

/* cart page */
// document.addEventListener('DOMContentLoaded', function () {
//   document.querySelectorAll('.cart-increment').forEach(button => {
//       button.addEventListener('click', function () {
//           let quantityElement = this.previousElementSibling;
//           let quantity = parseInt(quantityElement.textContent, 10);
//           quantityElement.textContent = quantity + 1;
//       });
//   });

//   document.querySelectorAll('.cart-decrement').forEach(button => {
//       button.addEventListener('click', function () {
//           let quantityElement = this.nextElementSibling;
//           let quantity = parseInt(quantityElement.textContent, 10);
//           if (quantity > 1) {
//               quantityElement.textContent = quantity - 1;
//           }
//       });
//   });
// });


document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll(".addToCartButton").forEach(button => {
        button.addEventListener('click', function() {
            let url = button.dataset.url;
            fetch(url, {
                method: 'POST',
                headers: {'X-CSRFToken': CSRF_TOKEN },
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) showToast('success', data.message);
                else showToast('error', "Error! add to cart failed.");
            })
            .catch(err => showToast('error', "Error! Something went wrong: " + err));
        });
    });
});



function confirmAction_old(options = {}) {
    const {
        title = 'Are you sure?',
        text = 'This action cannot be undone!',
        icon = 'warning',
        confirmText = 'Yes, proceed!',
        cancelText = 'Cancel',
        confirmColor = '#3085d6',
        cancelColor = '#d33',
        redirectUrl = null,
        onConfirm = null, // Optional callback
    } = options;

    Swal.fire({
        title,
        text,
        icon,
        showCancelButton: true,
        confirmButtonColor: confirmColor,
        cancelButtonColor: cancelColor,
        confirmButtonText: confirmText,
        cancelButtonText: cancelText,
    }).then((result) => {
        if (result.isConfirmed) {
            if (redirectUrl) {
                window.location.href = redirectUrl;
            } else if (typeof onConfirm === 'function') {
                onConfirm(); // Run callback if provided
            }
        }
    });
}


function confirmAction({
  title = 'Are you sure?',
  text = 'This action cannot be undone!',
  confirmText = 'Yes, proceed!',
  cancelText = 'Cancel',
  confirmUrl = null,
  onConfirm = null,
}) {
  Swal.fire({
    title: title,
    text: text,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: confirmText,
    cancelButtonText: cancelText,
    
    // 1. IMPORTANT: Disable SweetAlert's default button styling
    buttonsStyling: false, 

    confirmButtonColor: '#2563eb', 
    cancelButtonColor: '#6b7280', 

    customClass: {
      popup: 'rounded-2xl shadow-xl',
      confirmButton:
        'bg-primary-500 hover:bg-primary-600 text-white font-medium rounded-lg px-4 py-2 transition duration-150 ease-in-out shadow-md ml-3 rounded-full', 
      cancelButton:
        'bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium rounded-lg px-4 py-2 transition duration-150 ease-in-out',
    },
  }).then((result) => {
    if (result.isConfirmed) {
      if (confirmUrl) {
        window.location.href = confirmUrl;
      } else if (onConfirm && typeof onConfirm === 'function') {
        onConfirm();
      }
    }
  });
}


function showToast(type, message) {
    toastr.options = {
        "closeButton": true,
        "progressBar": true,
        "positionClass": "toast-top-right",
        "timeOut": "3000"
    };

    // type can be: success, info, warning, error
    toastr[type](message);
}