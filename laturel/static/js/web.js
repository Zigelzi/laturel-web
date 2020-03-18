document.addEventListener('DOMContentLoaded', () => {
    const contactForm = document.getElementById('contact-form');

    /** Send the data to given endpoint URL and redirect the user if it is wanted.
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
    /** Attaches the opening and closing function to all accordionItem:s */
    function attachAccordionToggling() {
        const accordionItems = document.getElementsByClassName('accordion-item');

        for (var i = 0; i < accordionItems.length; i++) {
            accordionItems[i].addEventListener('click', e => {
                toggleAccordionItem(e.currentTarget);
                
            })
        }
    }
    /** Toggles the accordionItem visibility with .active class
     * @param {HTMLElement} accordionItem Element with .accordion-item class
     */
    function toggleAccordionItem(accordionItem) {
        
        accordionItem.classList.toggle("active");
        accordionItem.nextElementSibling.classList.toggle("show");
    }

    /** Activates the navigation element where user is currently based on scroll position
     * @param {int} scrollPosition Current scroll position of the user
     */
    function activateNavSection(scrollPosition) {
        const topSectionPosition = 0;
        const servicesSection = document.getElementById('web-services-section');
        const contactFormSection = document.getElementById('contact-form-section');

        if (topSectionPosition <= scrollPosition) {
            highlightNavigation('home-link');
        }

        if (servicesSection.offsetTop <= scrollPosition) {
            highlightNavigation('services-link')
        }
        if (contactFormSection.offsetTop <= scrollPosition) {
            highlightNavigation('contact-form-link');
        }
        // If we're at the bottom of the page, highlight contact-information-section
        if (window.innerHeight + scrollPosition >= document.body.offsetHeight) {
            highlightNavigation('contact-information-link');
        }
    }
    /**Remove the .active-nav from previous active navigation item and add it to new active element
     * @param {string} activeElementId Name of the id of the element that will be highlighted
     */
    function highlightNavigation(activeElementId) {
        const activeClassName = 'active-nav'
        const navItemsArray = Array.from(document.getElementById('nav-list').children);
        const activeLink = document.getElementById(activeElementId);
        navItemsArray.forEach(element => {
            if (element.className === activeClassName) {
                element.classList.remove(activeClassName);
            }
        });
        activeLink.classList.add(activeClassName);
    }

    window.addEventListener('scroll', () => {
        activateNavSection(window.scrollY); 
    });

    contactForm.addEventListener('submit', e => {
        const envelope = document.getElementById('envelope');
        const formInputs = document.getElementById('form-inputs');

        e.preventDefault();
        
        contactForm.addEventListener('animationend', e => {
            // Collapse the form height when the send-envelope animation ends
            if (e.animationName === 'send-envelope') {
                formInputs.style.maxHeight = 0;
            }
        });

        // Start drawing the envelope and fade the form inputs away
        envelope.classList.add('send-envelope');
        formInputs.classList.add('hide-form');

        // Parse the <form id="contact-form"> element and send it to backend to be submitted
        sendForm('/', 'contact-form');
    });

    attachAccordionToggling();
})