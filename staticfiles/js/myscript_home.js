// $('#slider1, #slider2, #slider3').owlCarousel({
//     loop: true,
//     margin: 20,
//     nav: true,
//     dots: false,
//     responsiveClass: true,
//     responsive: {
//         0: {
//             items: 1,
//             autoplay: true
//         },
//         600: {
//             items: 2,
//             autoplay: true
//         },
//         1000: {
//             items: 4,
//             autoplay: true
//         }
//     }
// });

$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    nav: true,
    navText: [
      '<button class="btn position-absolute top-50 start-0 translate-middle-y z-1"><</button>',
      '<button class="btn position-absolute top-50 end-0 translate-middle-y z-1">></button>'
    ],
    dots: false,
    responsive: {
      0: { items: 1, autoplay: true },
      600: { items: 2, autoplay: true },
      1000: { items: 4, autoplay: true }
    }
  });

$('.plus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2] 
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity 
            document.getElementById("amount").innerText = "Rs. " + data.amount;
            document.getElementById("totalamount").innerText = "Rs. " + data.totalamount;

        }
    })
})

$('.minus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2] 
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity 
            document.getElementById("amount").innerText = "Rs. " + data.amount;
            document.getElementById("totalamount").innerText = "Rs. " + data.totalamount;

        }
    })
})


$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this;

    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
             prod_id: id
         },
        success: function(data){ 
            document.getElementById("amount").innerText = "Rs. " + data.amount;
            document.getElementById("totalamount").innerText = "Rs. " + data.totalamount;
            eml.closest('.cart-item').remove();

            if(data.cart_empty){
                $('.card-body').first().html(`
                    <div class="text-center p-5">
                        <h4 class="text-muted mt-3">Your cart is empty</h4>
                        <a href="/" class="btn btn-outline-primary mt-3">Start shopping</a>
                    </div>
                `);

                $('.col-lg-4 .card-body').html(`
                    <p class="text-muted text-center mt-4">Add a few items to see your price summary here.</p>
                `);
            }
        }
    });
});
