// REMOVE ITEM FORM CART
$(document).ready(function() {
        // Handle click event for the "Remove" button
        $('.remove-item').on('click', function() {
            const itemId = $(this).data('index'); // Get item ID from data attribute

            $.ajax({
                url: '/remove-from-cart/', // URL to the view
                method: 'POST',
                data: JSON.stringify({ 'product_id': itemId }),
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': getCSRFToken() // CSRF token for security
                },
                success: function(response) {
                    if (response.success) {
                        // Remove the item from the cart display
                        $(`div[data-item-id="${itemId}"]`).remove();
                        expense_update(response);

                        showPopup('Item removed successfully!', 'success');
                    } else {
                        showPopup('Failed to remove item.', 'error');
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Error:', error);
                    showPopup('Failed to remove item.', 'error');
                }
            });
        });
    });

// MARK/UNMARK ITEM AS BOUGHT
$(document).ready(function() {
        // handle checkbox change state
        $('.mark-bought').on('change', function() {
            const checkbox = $(this);
            const productId = checkbox.data('product-id');
            const isBought = checkbox.is(':checked');

            $.ajax({
                url: '/mark-as-bought/',
                method: 'POST',
                data: JSON.stringify({ 'product_id': productId, 'bought': isBought }),
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': getCSRFToken() // Include the CSRF token
                },
                success: function(response) {
                    if (response.success) {
                        if (isBought) {
                            // If the item is marked as bought, change the background color
                            checkbox.closest('.row').addClass('bg-success-subtle');

                            // Disable the number input field
                            checkbox.closest('.row').find('input[type="number"]').prop('disabled', true).addClass('disabled-field');

                        } else {
                            // If unchecked, revert the background color
                            checkbox.closest('.row').removeClass('bg-success-subtle');
                            // Enable the number input field
                            checkbox.closest('.row').find('input[type="number"]').prop('disabled', false).removeClass('disabled-field');
                        }
                    } else {
                        // handles the case where the server returns an error
                        showPopup('Failed to update item status.', 'error');
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Error:', error);
                    showPopup('Failed to update item status.', 'error');
                }
            });
        });
    });

// INCREASE/DECREASE ITEM QUANTITY IN CART
$(document).ready(function() {
    // Attaching an event listener to the quantity input fields
    $('.quantity-input').on('change', function() {
        const $input = $(this);
        const newQuantity = $input.val(); // Get the new quantity
        const productId = $input.parent().data('product-id'); // Get the item ID from the closest parent row

        $.ajax({
            url: '/update-quantity/',
            method: 'POST',
            data: JSON.stringify({
                'product_id': productId,
                'quantity': newQuantity
            }),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': getCSRFToken() // CSRF token for security
            },
            success: function(response) {
                if (response.success) {
                    expense_update(response); // update expenses i.e. total price, exceeding amount
                    showPopup('Quantity updated successfully.', 'success');
                } else {
                    showPopup('Failed to update quantity.', 'error');
                }
            },
            error: function(xhr, status, error) {
                showPopup(error.toString(), 'error');
            }
        });
    });
});

//UTILITY FUNCTION TO UPDATE TOTAL PRICE AND EXCEEDING AMOUNT
function expense_update(response) {
        $('#total-price').text(response.total_price);
        if(response.exceeds_limit){
            $('#exceed-amount').text(response.exceed_amount);
            $('#exceed-amount').parent().attr('hidden', false);
        }
        else{
            $('#exceed-amount').parent().attr('hidden', true);
        }
    }


///////Initializing Sortable.js for enabling drag up/down for cart items' reordering////////
document.addEventListener('DOMContentLoaded', function() {
    var cartItemsContainer = document.getElementById('cart-items-container');

    // Initialize Sortable.js
    var sortable = new Sortable(cartItemsContainer, {
        animation: 150,
        handle: '.draggable-item', // Allow dragging of the entire item
        onEnd: function(event) {
            // The order has been changed
            var order = [];
            document.querySelectorAll('.draggable-item').forEach(function(item) {
                order.push(item.getAttribute('data-item-id'));
            });
            // Send AJAX request to update order in the backend
            $.ajax({
                url: '/update-cart-order/',
                method: 'POST',
                data: JSON.stringify({order: order}),
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': getCSRFToken() // get CSRF token for security
                },
                success: function(response) {
                    if (response.success) {
                        showPopup('Order updated successfully', 'success');
                    } else {
                        showPopup('Failed to update order', 'error');
                    }
                },
                error: function(xhr, status, error) {
                    showPopup(error.toString(), 'error');
                }
            });
        }
    });
});

// SHARE CART VIA EMAIL
$(document).ready(function() {
    $('#shareCartForm').on('submit', function(event) {
        event.preventDefault();

        var email = $('#email').val();
        var shoppingListId = $('#shopping_list_id').val();

        $.ajax({
            url: '/share-cart/',
            method: 'POST',
            data: {
                email: email,
                shopping_list_id: shoppingListId,
            },
            headers: {
                'X-CSRFToken': getCSRFToken() // CSRF token for security
            },
            success: function(response) {
                if (response.success) {
                    $('#shareCartMessage').html('<div class="alert alert-success">Cart shared successfully!</div>');
                    $('#email').val('');
                } else {
                    $('#shareCartMessage').html('<div class="alert alert-danger">Error: ' + response.message + '</div>');
                }
            },
            error: function() {
                $('#shareCartMessage').html('<div class="alert alert-danger">An unexpected error occurred.</div>');
            }
        });
    });
});


