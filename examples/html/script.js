// Initialize the required DOM elements
const navbarMenu = document.getElementById("menu");
const burgerMenu = document.getElementById("burger");
const headerMenu = document.getElementById("header");
const bgOverlay = document.querySelector(".overlay");

// Initialize hide navbar menu function
const toggleNavbarMenu = () => {
   navbarMenu.classList.toggle("is-active");
   burgerMenu.classList.toggle("is-active");
   bgOverlay.classList.toggle("is-active");
};

// Show hide toggle navbar menu on clicked
burgerMenu.addEventListener("click", () => {
   toggleNavbarMenu();
});

// Hide the navbar menu when overlay clicked
bgOverlay.addEventListener("click", () => {
   toggleNavbarMenu();
});

// Hide the navbar menu when links clicked
document.querySelectorAll(".menu-link").forEach((link) => {
   link.addEventListener("click", () => {
      toggleNavbarMenu();
   });
});

// Change the header background on scrolling
window.addEventListener("scroll", () => {
   if (window.scrollY >= 75) {
      headerMenu.classList.add("on-scroll");
   } else {
      headerMenu.classList.remove("on-scroll");
   }
});

// Fixed the navbar menu on window resizing
window.addEventListener("resize", () => {
   if (window.innerWidth >= 768) {
      if (navbarMenu.classList.contains("is-active")) {
         navbarMenu.classList.remove("is-active");
         burgerMenu.classList.remove("is-active");
         bgOverlay.classList.remove("is-active");
      }
   }
});

// Carousel functionality
const slides = document.querySelectorAll('.carousel-slide');
const indicators = document.querySelectorAll('.indicator');
let currentSlide = 0;

// Function to show specific slide
const showSlide = (index) => {
   // Remove active class from all slides and indicators
   slides.forEach(slide => slide.classList.remove('active'));
   indicators.forEach(indicator => indicator.classList.remove('active'));
   
   // Add active class to current slide and indicator
   slides[index].classList.add('active');
   indicators[index].classList.add('active');
   
   currentSlide = index;
};

// Auto-play carousel
const autoPlay = () => {
   currentSlide = (currentSlide + 1) % slides.length;
   showSlide(currentSlide);
};

// Start auto-play
let autoPlayInterval = setInterval(autoPlay, 4000);

// Click event for indicators
indicators.forEach((indicator, index) => {
   indicator.addEventListener('click', () => {
      clearInterval(autoPlayInterval);
      showSlide(index);
      // Restart auto-play after manual selection
      autoPlayInterval = setInterval(autoPlay, 4000);
   });
});

// Pause auto-play on hover
const carousel = document.querySelector('.carousel-container');
if (carousel) {
   carousel.addEventListener('mouseenter', () => {
      clearInterval(autoPlayInterval);
   });

   carousel.addEventListener('mouseleave', () => {
      autoPlayInterval = setInterval(autoPlay, 4000);
   });
}