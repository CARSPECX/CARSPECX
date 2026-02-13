// Load all cars globally
let cars = [];

// Fetch cars once
fetch("data/cars.json")
  .then(res => res.json())
  .then(data => {
      cars = data;
      console.log("Cars loaded:", cars.length);
  });

// Utility: get car by ID
function getCarById(id){
    return cars.find(c => c.ID == id);
}

// Utility: format price
function formatPrice(p){
    return "₹" + p.toLocaleString();
}
