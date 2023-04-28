$(function() {
  "use strict";

  //------- Parallax -------//
  skrollr.init({
    forceHeight: false
  });

  //------- Active Nice Select --------//
  $('select').niceSelect();

  //------- hero carousel -------//
  $(".hero-carousel").owlCarousel({
    items:3,
    margin: 10,
    autoplay:false,
    autoplayTimeout: 5000,
    loop:true,
    nav:false,
    dots:false,
    responsive:{
      0:{
        items:1
      },
      600:{
        items: 2
      },
      810:{
        items:3
      }
    }
  });

  //------- Best Seller Carousel -------//
  if($('.owl-carousel').length > 0){
    $('#bestSellerCarousel').owlCarousel({
      loop:true,
      margin:30,
      nav:true,
      navText: ["<i class='ti-arrow-left'></i>","<i class='ti-arrow-right'></i>"],
      dots: false,
      responsive:{
        0:{
          items:1
        },
        600:{
          items: 2
        },
        900:{
          items:3
        },
        1130:{
          items:4
        }
      }
    })
  }

  //------- single product area carousel -------//
  $(".s_Product_carousel").owlCarousel({
    items:1,
    autoplay:false,
    autoplayTimeout: 5000,
    loop:true,
    nav:false,
    dots:false
  });

  //------- mailchimp --------//  
	function mailChimp() {
		$('#mc_embed_signup').find('form').ajaxChimp();
	}
  mailChimp();
  
  //------- fixed navbar --------//  
  $(window).scroll(function(){
    var sticky = $('.header_area'),
    scroll = $(window).scrollTop();

    if (scroll >= 100) sticky.addClass('fixed');
    else sticky.removeClass('fixed');
  });

  //------- Price Range slider -------//
  if(document.getElementById("price-range")){
  
    var nonLinearSlider = document.getElementById('price-range');
    
    noUiSlider.create(nonLinearSlider, {
        connect: true,
        behaviour: 'tap',
        start: [ 500, 4000 ],
        range: {
            // Starting at 500, step the value by 500,
            // until 4000 is reached. From there, step by 1000.
            'min': [ 0 ],
            '10%': [ 500, 500 ],
            '50%': [ 4000, 1000 ],
            'max': [ 10000 ]
        }
    });
  
  
    var nodes = [
        document.getElementById('lower-value'), // 0
        document.getElementById('upper-value')  // 1
    ];
  
    // Display the slider value and how far the handle moved
    // from the left edge of the slider.
    nonLinearSlider.noUiSlider.on('update', function ( values, handle, unencoded, isTap, positions ) {
        nodes[handle].innerHTML = values[handle];
    });
  
  }
  
});


// $('.plus-cart').click(function(){
//   var pid = $(this).attr("pid").toString();
//   var vid = $(this).attr("vid").toString(); // get the variation ID
//   var eml = this.parentNode.children[1];
//   $.ajax({
//       type: "GET",
//       url: "pluscart",
//       data: {
//           prod_id: pid,
//           var_id: vid // pass the variation ID
//       },
//       success: function(data) {
//           eml.innerText = data.quantity;
//           document.getElementById("amount").innerText = data.amount;
//           document.getElementById("total_amount").innerText = data.total_amount;
//       }
//   });
// });


$('.plus-cart').click(function(){
  var pid = $(this).attr("pid").toString();
  var vid = $(this).attr("vid").toString();
  var eml = this.parentNode.children[1];
  
  $.ajax({
      type: "GET",
      url: "pluscart",
      data: {
          prod_id: pid,
          var_id: vid
      },
      success: function(data) {
          if (data.error) {
              alert(data.error); // show the error message
          } else {
              eml.innerText = data.quantity;
              document.getElementById("amount").innerText = data.amount;
              document.getElementById("total_amount").innerText = data.total_amount;
          }
      },
      error: function(xhr, status, error) {
          console.log(xhr.responseText); // log any errors to the console
      }
  });
});


    // minus cart quantity
    $('.minus-cart').click(function(){
      var pid = $(this).attr("pid").toString();
      var vid = $(this).attr("vid").toString(); // get the variation ID
      var eml = this.parentNode.children[1];
      $.ajax({
          type: "GET",
          url: "minuscart",
          data: {
              prod_id: pid,
              var_id: vid // pass the variation ID
          },
          success: function(data) {
              if (data.quantity == 0) {
                  eml.parentNode.parentNode.parentNode.parentNode.removeChild(eml.parentNode.parentNode.parentNode);
                  alert("Item removed from cart.");
              } else {
                  eml.innerText = data.quantity;
              }
              document.getElementById("amount").innerText = data.amount;
              document.getElementById("total_amount").innerText = data.total_amount;
          }

      });
  });



$('.remove-cart').click(function(){
  var prod_id = $(this).attr("pid").toString();
  var var_id = $(this).attr("vid");
  console.log(prod_id,'hi')
  var_id = var_id.replace('[','').replace(']','').replace("'","").replace('"',''); // Add this line
  var eml = this;
  
  if (confirm("Are you sure you want to delete this item?")) {
    $.ajax({
      type: "GET",
      url: "removecart",
      data: {
        prod_id: prod_id,
        var_id: var_id
      },
      success: function(data) {
        
        document.getElementById("amount").innerText = data.amount;
        document.getElementById("total_amount").innerText = data.total_amount;
        eml.parentNode.parentNode.remove();
        $('.product-image').filter('[data-product-id="' + prod_id + '"]').remove();
        $('.product-details').filter('[data-product-id="' + prod_id + '"]').remove();
      }
    });
  }
});



$(document).ready(function(){
  $(".ajaxLoader").hide();

  // Filter and search event listener
  $(".pixel-radio, #search-button").on('click',function(){
    var _filterObj={};
    $(".pixel-radio").each(function(index,ele){
      var _filterVal=$(this).val();
      var _filterKey=$(this).data('filter');
      _filterObj[_filterKey]=Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(ele){
        return ele.value;
      });
    });

    // Get search query
    var searchQuery = $("#search-input").val().trim();
    // console.log(searchQuery)
    // Add search query to data object
    if (searchQuery) {
      _filterObj['q'] = searchQuery;
    }

    // Run AJAX
    $.ajax({
      url:'filter-data',
      data:_filterObj,
      dataType:'json',
      beforeSend:function(){
        $(".ajaxLoader").show();
      },
      success:function(res){
        // console.log(res)
        $("#filteredProducts").html(res.data);
        $(".ajaxLoader").hide();
      }
    });
    // console.log(_filterObj)
  });
});


$(document).ready(function(){
  $(".ajaxLoader").hide();

  // Filter and search event listener
  $(".pixel-radio, #search-button, #sort-by").on('change',function(){
      var _filterObj={};
      $(".pixel-radio").each(function(index,ele){
          var _filterVal=$(this).val();
          var _filterKey=$(this).data('filter');
          _filterObj[_filterKey]=Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(ele){
              return ele.value;
          });
      });

      // Get search query
      var searchQuery = $("#search-input").val().trim();
      // console.log(searchQuery)
      // Add search query to data object
      if (searchQuery) {
          _filterObj['q'] = searchQuery;
      }

      // Get sort option
      var sortOption = $("#sort-by").val();
      // Add sort option to data object
      if (sortOption) {
          _filterObj['sort'] = sortOption;
      }

      // Run AJAX
      $.ajax({
          url:'filter-data',
          data:_filterObj,
          dataType:'json',
          beforeSend:function(){
              $(".ajaxLoader").show();
          },
          success:function(res){
              // console.log(res)
              $("#filteredProducts").html(res.data);
              $(".ajaxLoader").hide();
          }
      });
      // console.log(_filterObj)
  });
});


// add wishlist



$(document).ready(function(){
  $(document).on('click',".add-wishlist",function(){
    var _pid=$(this).attr('data-product');
    var _vm=$(this)
    //console.log(_pid)
    $.ajax({
      url:"/whishlist/",
      data:{
        product_id:_pid
      },
      dataType:'json',
      success:function(res){
        console.log('hi')
        if(res.bool==true){
          _vm.addClass('disabled').removeClass('add-wishlist');
          // alert('Product added to wishlist');
        }
      }

    });
  });
});

