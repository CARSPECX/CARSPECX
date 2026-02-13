// Load all cars globally
let CARS = [];

// Fetch cars once
fetch("CARS.json")
  .then(res => res.json())
  .then(data => {
      CARS = data;
      console.log("Cars loaded:", CARS.length);
  });
.catch(err => console.error("Failed to load cars.json:", err));
// Utility: get car by ID
function getCarById(id){
    return CARS.find(c => c.id == id);
}

// Utility: format price
function formatPrice(p){
    return "₹" + p.toLocaleString();
}
