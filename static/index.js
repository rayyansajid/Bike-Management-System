const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");
const themeToggler = document.querySelector(".theme-toggle-btn");

// Show sidebar
menuBtn.addEventListener("click", () => {
  sideMenu.style.display = "block";
});


// Close sidebar
closeBtn.addEventListener("click", () => {
  sideMenu.style.display = "none";
});

// Switch theme
themeToggler.addEventListener("click", () => {
  document.body.classList.toggle('dark-theme-variables')

  themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
  themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');
});

// // Fill orders in table
// Orders.forEach(order => {
//   const tr = document.createElement('tr');
//   const trContent = `
//               <td>${order.ClientName}</td>
//               <td>${order.packageNumber}</td>
//               <td class = "${order.packageStatus === "Declined" ? 'danger' : order.packageStatus === 'Pending' ? 'warning' : 'primary'}">${order.packageStatus}</td>
//               <td class = "primary">Details</td>
//              `
//   tr.innerHTML = trContent;
//   document.querySelector('table tbody').appendChild(tr);
// });