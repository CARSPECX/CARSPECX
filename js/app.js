// Load all cars globally
let CARS = [];

// Fetch cars once
fetch("data/cars.json")
  .then(res => res.json())
  .then(data => {
      CARS = data;
      console.log("Cars loaded:", CARS.length);
  });

// Utility: get car by ID
function getCarById(id){
    return CARS.find(c => c.ID == id);
}

// Utility: format price
function formatPrice(p){
    return "₹" + p.toLocaleString();
}
