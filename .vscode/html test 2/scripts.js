// Form submission handling
document.getElementById('contact-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const submitButton = this.querySelector('button[type="submit"]');
    const originalText = submitButton.innerHTML;
    
    // Show loading state
    submitButton.innerHTML = '<i class="bx bx-loader bx-spin"></i> Sending...';
    submitButton.disabled = true;

    try {
        // Simulate form submission (replace with actual API call)
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // Clear form
        this.reset();
        alert('Message sent successfully!');
    } catch (error) {
        alert('Error sending message. Please try again.');
    } finally {
        // Restore button state
        submitButton.innerHTML = originalText;
        submitButton.disabled = false;
    }
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Social icons hover animation
document.querySelectorAll('.social-links a').forEach(link => {
    link.addEventListener('mouseenter', function() {
        const icon = this.querySelector('.bx');
        icon.classList.add('bx-tada');
    });
    
    link.addEventListener('mouseleave', function() {
        const icon = this.querySelector('.bx');
        icon.classList.remove('bx-tada');
    });
});

// Form validation
const formInputs = document.querySelectorAll('#contact-form input, #contact-form textarea');

formInputs.forEach(input => {
    input.addEventListener('blur', function() {
        if (!this.value) {
            this.classList.add('invalid');
        } else {
            this.classList.remove('invalid');
        }
    });
    
    input.addEventListener('focus', function() {
        this.classList.remove('invalid');
    });
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Add any initialization code here
});