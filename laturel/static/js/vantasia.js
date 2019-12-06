document.addEventListener('DOMContentLoaded', () => {
    const navHamburger = document.getElementById('nav-hamburger-container');
    const vantasiaSection = document.getElementById('vantasia');
    const navMenu = document.getElementById('nav-menu');
    const contactForm = document.getElementById('contact-form');
    const envelope = document.getElementById('envelope');
    const formInputs = document.getElementById('form-inputs');
    const accordionItems = document.getElementsByClassName('accordion-item');
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

    /**
     * 
     * @param {HTMLCollection} elements Collection of elements being toggled
     * @param {string} className String of class name that is being toggled.
     * @param {string} methodName Name of method which is being used.
     */
    function setClass(elements, className, methodName) {
        for (var i = 0; i < elements.length; i++) {
            elements[i].classList[methodName](className);
        }
    }

    try {
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
    } catch (error) {
        console.log(error);
        if (error instanceof ReferenceError) {
            console.log(error);
        }
    }
    
    function toggleNav() {
        // Open and close the mobile navigation
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

    window.addEventListener('scroll', () => {
        if (vantasiaSection.offsetTop > window.scrollY) {
            navHamburger.style.background = "rgba(75, 75, 75, 0.2)"
        } else {
            navHamburger.style.background = "rgba(75, 75, 75, 0.0)"
        }
    });

    window.addEventListener('scroll', () => {
        if (window.scrollY > 5) {
            navMenu.style.background = "rgba(75, 75, 75, 0.9)"
        } else if (window.innerWidth > 768 ) {
            navMenu.style.background = "rgba(75, 75, 75, 0.0)"
        }
    })
})