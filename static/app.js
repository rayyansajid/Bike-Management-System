const selectBox = document.querySelector('#prod-sel-box');
const selectOption = document.querySelector('#prod-sel-option');
const soValue = document.querySelector('#soValue');
const optionSearch = document.querySelector('#optionSearch');
const items = document.querySelectorAll("#prod-sel-box .checkbox");
const items2 = document.querySelectorAll("#prod-sel-box .item")


selectOption.addEventListener('click', function() {
  selectBox.classList.toggle('active');
});

items.forEach(item => {
  item.addEventListener('click', (event) => {
    const target = event.target;
    if (!target.classList.contains('quantity-input')) {
      item.classList.toggle('checked');

      let checked = document.querySelectorAll("#prod-sel-box .checked");

      if (checked && checked.length > 0) {
        soValue.value = `${checked.length} selected`;
      } else {
        soValue.value = "Select Products";
      }
    }
  });
});

// Searching feature 
optionSearch.addEventListener('keyup', () => {
  const searchTerm = optionSearch.value.toLowerCase();

  items2.forEach(item => {
    const textSpanName = item.querySelector(".prod-name");
    const textSpanType = item.querySelector(".prod-type");
    const textName = textSpanName.textContent.toLowerCase();
    const textType = textSpanType.textContent.toLowerCase();

    if (textName.includes(searchTerm) || textType.includes(searchTerm)) {
      item.style.display = '';
    } else {
      item.style.display = 'none';
    }
  });
})
