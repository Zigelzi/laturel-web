document.addEventListener('DOMContentLoaded', () => {
    const navHamburger = document.getElementById('nav-hamburger-container')

    function adjustNavTransparency(scrollPosition) {
        const navMenu = document.getElementById('nav-menu');
        const navBarHeight = 50;
        const navBackgroundClass = 'nav-menu-blue'
        
        if (scrollPosition > navBarHeight) {
            navMenu.classList.add(navBackgroundClass);
        } else {
            navMenu.classList.remove(navBackgroundClass);
        }
    }
    
    function toggleNav() {
        // Open and close the mobile navigation
        const navMenu = document.getElementById('nav-menu');
        navHamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    }
    
    function attachNavToggling() {
        const navItems = document.getElementById('nav-list').children;
        for (let i = 0; i < navItems.length; i++) {
            // Loop though all the <li> items in nav and attach toggling the nav on click on <a> (children[0]) element.
            navItems[i].children[0].addEventListener('click', () => {
                toggleNav()
            });
        }
    }

    function adjustNavHamburgerTransparency(scrollPosition) {
        const servicesSection = document.getElementById('web-services-section');

        if (servicesSection !== null) {
            if (scrollPosition > servicesSection.offsetTop) {
                navHamburger.style.background = "rgba(75, 75, 75, 0.2)"
            } else {
                navHamburger.style.background = "rgba(75, 75, 75, 0.0)"
            }
        } else {
            navHamburger.style.background = "rgba(75, 75, 75, 0.2)"
        }
        
    }

    

    navHamburger.addEventListener('click', () => {
        toggleNav()
    });

    window.addEventListener('scroll', () => {
        adjustNavTransparency(window.scrollY);
        adjustNavHamburgerTransparency(window.scrollY);
    });

    attachNavToggling();
})


