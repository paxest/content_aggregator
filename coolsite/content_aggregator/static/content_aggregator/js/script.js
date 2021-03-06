// menu script
const menuButton = document.querySelector('.header__burger');
const menu = document.querySelector('.header__nav');

menuButton.addEventListener("click", function() {
    let width = document.documentElement.clientWidth;
    let menuItems = menu.querySelectorAll('.main-menu__text')
    
    if (window.getComputedStyle(menu).display == 'none') {
        menu.style.display = 'flex'
    }
    
    if (menuButton.classList.contains('active')) {
        menuItems.forEach(item => item.style.display = 'none');
        menuButton.classList.remove('active')
        menu.classList.remove('active')
        if (width <= 650) {
            menu.style.display = 'none'
            console.log(width)
        }
    } else {
        menuItems.forEach(item => item.style.display = 'inline-block');
        menuButton.classList.add('active')
        menu.classList.add('active')
    }
});

// change categories script
const categoriesItems = document.querySelectorAll('.categories__item');
const categoriesInfoItemsSelected = document.querySelectorAll('.categories__item-info_selected')
const button = document.querySelector('.button');
const listCategories = [];


if (categoriesInfoItemsSelected.length != 0) {
    button.removeAttribute('disabled')
    categoriesInfoItemsSelected.forEach(item => {
        let itemCheckbox = item.parentNode.firstElementChild;
        itemCheckbox.checked = 1;
        listCategories.push(itemCheckbox);
    });
}


categoriesItems.forEach(item => {
    let itemCheckbox = item.firstElementChild;
    let itemLabel = item.lastElementChild;
    itemLabel.addEventListener("click", function() {
        if (itemCheckbox.checked) {
            itemLabel.classList.remove('categories__item-info_selected');
            itemCheckbox.checked = 1;

            itemCheckboxIndex = listCategories.indexOf(itemCheckbox);
            if (itemCheckboxIndex != -1) {
                listCategories.splice(itemCheckboxIndex, 1);
            }
            
        } else {
            itemLabel.classList.add('categories__item-info_selected');
            itemCheckbox.checked = 0;
            listCategories.push(itemCheckbox);
        }

        if (listCategories.length != 0) {
            button.removeAttribute('disabled')
        } else {
            button.setAttribute('disabled', 'disabled')
        }
    });
});


button.addEventListener("click", function() {
    console.log(listCategories)
});