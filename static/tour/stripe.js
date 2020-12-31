// static/main.js

//window.alert(client_id);
//window.alert(deposit);

console.log("Sanity check!");

// Get Stripe publishable key
fetch("/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);

  // new
  // Event handler
 // document.querySelector("#submitBtn").addEventListener("click", () => {
    // Get Checkout Session ID
    //print("/create-checkout-session/" + client_id + "/" + deposit)
    fetch("/create-checkout-session/" + client_id + "/" + deposit)
        
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  //});
});