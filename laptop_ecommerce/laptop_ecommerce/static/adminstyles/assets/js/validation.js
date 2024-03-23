// validation.js

function validateProductName() {
    var productName = document.getElementById('product_name').value.trim();

    // Test Case: Valid Name
    if (!/^[A-Za-z\s]+$/.test(productName)) {
        alert('Test Case Failed: Enter a valid name with letters and spaces.');
        return false;
    } 

    // Test Case: Empty Name
    if (productName === '') {
        alert('Test Case Failed: Leave the name field empty.');
        return false;
    }

    // Test Case: Name with Digits
    if (/\d/.test(productName)) {
        alert('Test Case Failed: Enter a name with digits.');
        return false;
    }

    // Test Case: Name with Special Characters
    if (!/^[A-Za-z\s]+$/.test(productName)) {
        alert('Test Case Failed: Enter a name with special characters.');
        return false;
    }

    // Test Case: Name with Length Limit
    if (productName.length >= 20) {
        alert('Test Case Failed: Enter a name exceeding the character limit.');
        return false;
    }

    // Test Case: No Leading Spaces
    if (/^\s/.test(productName)) {
        alert('Test Case Failed: Remove leading spaces from the name.');
        return false;
    }
    // Test Case: Name with HTML/Script Tags
    if (/<[^>]*>/i.test(productName)) {
        alert('Test Case Failed: Try injecting HTML or script tags in the name.');
        return false;
    }

    // Test Case: Name with Multiple Spaces
    if (/\s{2,}/.test(productName)) {
        alert('Test Case Failed: Enter multiple consecutive spaces in the name.');
        return false;
    }

    // Test Case: Name with Line Breaks
    if (/\n|\r/.test(productName)) {
        alert('Test Case Failed: Enter a name with line breaks.');
        return false;
    }

    // Test Case: Name with Valid Length
    if (productName.length <= 5) {
        alert('Test Case Failed: Enter a name with a valid length.');
        return false;
    }

    // All test cases passed
    return true;
}
