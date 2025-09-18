console.log("Running main.js...");

// get stripe publishable key
fetch("/config")
  .then((result) => result.json())
  .then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);

    // Event handler
    document.querySelector("#submitBtn").addEventListener("click", (e) => {
      const businessId = e.target.dataset.businessId;

      // Get Checkout Session ID
      fetch(`/business/${businessId}/create_checkout_session`)
        .then((result) => result.json())
        .then((data) => {
          console.log(data);
          // Redirect to Stripe Checkout
          return stripe.redirectToCheckout({ sessionId: data.sessionId });
        })
        .then((res) => {
          console.log(res);
        });
    });
  });