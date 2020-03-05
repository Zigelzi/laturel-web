document.addEventListener('DOMContentLoaded', () => {
    const navHamburger = document.getElementById('nav-hamburger-container')
    const contactForm = document.getElementById('contact-form');
    const envelope = document.getElementById('envelope');
    const formInputs = document.getElementById('form-inputs');
    const accordionItems = document.getElementsByClassName('accordion-item');
    const accordionPanels = document.getElementsByClassName('accordion-panel');
    const navItems = document.getElementById('nav-list').children;

    /** Send the data to given endpoint URL and redirect the user if it is wanted.
     * 
     * @param {string} url Endpoint URL where the data is sent to
     * @param {json} jsonObject JSON Object of the data that is being sent
     * @param {string} csrfToken CSRF token value if the form has it enabled
     * @param {boolean} redirect Will the user be redirected after the data is submitted
     */
    function sendData(url, jsonObject, csrfToken=null, redirect=false) {
        const xhr = new XMLHttpRequest();
        const jsonData = JSON.stringify(jsonObject);
    
        xhr.open('POST', url);
        if (csrfToken !== null) {
            xhr.setRequestHeader('X-CSRFToken', csrfToken);
        }
        if (redirect === true) {
            // If redirect is true then redirect the user to url returned by the backend
            xhr.onreadystatechange = () => {
                if (xhr.readyState === 4) {
                    const redirectUrl = JSON.parse(xhr.response);
                    window.location.replace(redirectUrl.redirect);
                }
            }
        }
        xhr.setRequestHeader('Content-type', 'application/json');
        xhr.send(jsonData);
    }

    /** Parse the <form> element and create JSON object to be sent to backend.
     * 
     * @param {string} url Endpoint URL where the form will be sent
     * @param {string} formElementId Element ID of the <form> element that is being sent
     */
    function sendForm(url, formElementId) {
        const form = document.getElementById(formElementId);
        const formData = new FormData(form);
        const jsonObject = new Object();
        formData.forEach((value, key) => {
            jsonObject[key] = value;
        })
        sendData(url, jsonObject, jsonObject.csrf_token, false);
    }

    try {
        window.addEventListener('scroll', () => {

            activateNavSection(window.scrollY);
            adjustNavTransparency(window.scrollY);
            
        });
        if (contactForm !== null) {
            const servicesSection = document.getElementById('web-services-section');

            if (servicesSection.offsetTop < window.scrollY) {
                navHamburger.style.background = "rgba(75, 75, 75, 0.2)"
            } else {
                navHamburger.style.background = "rgba(75, 75, 75, 0.0)"
            }
            contactForm.addEventListener('submit', e => {
                e.preventDefault()
                
                contactForm.addEventListener('animationend', (e) => {
                    // Collapse the form height when the send-envelope animation ends
                    if (e.animationName === 'send-envelope') {
                        formInputs.style.maxHeight = 0;
                    }
                });
                // Start drawing the envelope and fade the form inputs away
                envelope.classList.add('send-envelope');
                formInputs.classList.add('hide-form');
        
                // Parse the <form id="contact-form"> element and send it to backend to be submitted
                sendForm('/', 'contact-form')
            });
        }
        
        
    } catch (error) {
        console.log(error);
        if (error instanceof ReferenceError) {
            console.log(error);
        }
    }

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
    function activateNavSection(scrollPosition) {
        // Activates the navigation element where user is currently based on scroll position
        const topSectionPosition = 0;
        const servicesSection = document.getElementById('web-services-section');
        const contactFormSection = document.getElementById('contact-form-section');
        const contactInformationSection = document.getElementById('contact-information-section');

        if (servicesSection === null || contactFormSection === null) {
            return;
        }
        if (topSectionPosition <= scrollPosition) {
            highlightNavigation('home-link')
        }

        if (servicesSection.offsetTop <= scrollPosition) {
            highlightNavigation('services-link')
        }
        if (contactFormSection.offsetTop <= scrollPosition) {
            highlightNavigation('contact-form-link')
        }
        // If we're at the bottom of the page, highlight contact-information-section
        if (window.innerHeight + scrollPosition >= document.body.offsetHeight) {
            highlightNavigation('contact-information-link')
        }
    }

    function highlightNavigation(activeElementId) {
        // Remove the .active-nav from previous active navigation item and add it to new active element
        const activeClassName = 'active-nav'
        const navItemsArray = Array.from(document.getElementById('nav-list').children);
        navItemsArray.forEach(element => {
            if (element.className === activeClassName) {
                element.classList.remove(activeClassName)
            }
        });
        const activeLink = document.getElementById(activeElementId);
        activeLink.classList.add(activeClassName);
    }
    
    function toggleNav() {
        // Open and close the mobile navigation
        const navMenu = document.getElementById('nav-menu');
        navHamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    }

    navHamburger.addEventListener('click', () => {
        toggleNav()
    });

    for (let i = 0; i < navItems.length; i++) {
        // Loop though all the <li> items in nav and attach toggling the nav on click on <a> (children[0]) element.
        navItems[i].children[0].addEventListener('click', () => {
            toggleNav()
        });
    }

    for (var i = 0; i < accordionItems.length; i++) {
        accordionItems[i].onclick = function() {
                this.classList.toggle("active");
                this.nextElementSibling.classList.toggle("show");
        }
    }
})