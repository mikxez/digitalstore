const orderBtn = document.querySelector('.my_orders')
    const listOrders = document.querySelector('.list_orders')
    const arrowDown = document.querySelector('.errow_down')
    orderBtn.addEventListener('click', () => {
      listOrders.classList.toggle('active')
      arrowDown.classList.toggle('active')
    })

try {
    let heart = [...document.querySelectorAll('.link_fav')];

    heart.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            item.classList.toggle('active');
        });
    });

} catch (error) { }