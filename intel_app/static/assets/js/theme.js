/* Sticky Navigation */
$(function() {

  var sticky = $('.sticky');
  var contentOffset;
  var nav_height;

  if (sticky.length) {

    if ( sticky.data('offset') ) {
      contentOffset = sticky.data('offset');
    }
    else {
      contentOffset = sticky.offset().top;
    }
    nav_height = sticky.height();
  }

  var scrollTop = $(window).scrollTop();
  var window_height = $(window).height();
  var doc_height = $(document).height();

  $(window).bind('resize', function() {
    scrollTop = $(window).scrollTop();
    window_height = $(window).height();
    doc_height = $(document).height();
    navHeight();
  });

  $(window).bind('scroll', function() {
    stickyNav();
  });

  function navHeight() {
    sticky.css('max-height', window_height + 'px');
  }

  function stickyNav() {
    scrollTop = $(window).scrollTop();
    if (scrollTop > contentOffset) {
      sticky.addClass('fixed');
    }
    else {
      sticky.removeClass('fixed');
    }
  }

});

$('document').ready(function() {
  var nav_height = 70;

  $("a[data-role='smoothscroll']").click(function(e) {
    e.preventDefault();

    var position = $($(this).attr("href")).offset().top - nav_height;

    $("body, html").animate({
      scrollTop: position
    }, 1000 );
    return false;
  });
});

$('document').ready(function() {
  // Back to top
  var backTop = $(".back-to-top");

  $(window).scroll(function() {
    if($(document).scrollTop() > 400) {
      backTop.css('visibility', 'visible');
    }
    else if($(document).scrollTop() < 400) {
      backTop.css('visibility', 'hidden');
    }
  });

  backTop.click(function() {
    $('html').animate({
      scrollTop: 0
    }, 1000);
    return false;
  });
});


$('document').ready(function() {

  // Loader
  $(window).on('load', function() {
    $('.loader-container').fadeOut();
  });

  // Tooltips
  $('[data-toggle="tooltip"]').tooltip();

  // Popovers
  $('[data-toggle="popover"]').popover();

  // Page scroll animate
  new WOW().init();
});

$('document').ready(function() {
  $('#testimonials').owlCarousel({
    items: 1,
    loop: true,
    autoplay: true,
    autoplayHoverPause: true,
    animateOut: 'fadeOut',
    animateIn: 'fadeIn',
  });
});


/*
 *  Counter
 *
 *  Require(" jquery.animateNumber.min.js ", " jquery.waypoints.min.js ")
 */
$(document).ready(function() {
  var counterInit = function() {
    if ( $('.counter-section').length > 0 ) {
      $('.counter-section').waypoint( function( direction ) {

        if( direction === 'down' && !$(this.element).hasClass('animated') ) {

          var comma_separator_number_step = $.animateNumber.numberStepFactories.separator(',')
          $('.number').each(function(){
            var $this = $(this),
              num = $this.data('number');
            $this.animateNumber(
              {
                number: num,
                numberStep: comma_separator_number_step
              }, 5000
            );
          });

        }

      } , { offset: '95%' } );
    }

  }

  counterInit();
});


$(document).ready(function() {
  console.log("ready")
   $(".inc-btnn").off('click').on('click', function (e) {
  e.preventDefault();

  let inc_value = $(this).closest(".card-body").find(".qty-val").val();
  let value = parseInt(inc_value, 10);
  value = isNaN(value) ? 0 : value;

  if (value < 10) {
    value++;
    $(this).closest(".card-body").find(".qty-val").val(value);
  }
});


  $(".dec-btnn").off('click').on('click', function (e) {
  e.preventDefault();

  let dec_value = $(this).closest(".card-body").find(".qty-val").val();
  let value = parseInt(dec_value, 10);
  value = isNaN(value) ? 0 : value;

  if (value > 1) {
    value--;
    $(this).closest(".card-body").find(".qty-val").val(value);
  }
});


  $(".addToCartt").off('click').on('click', function (e) {
    e.preventDefault();

    var product_id = $(this).closest(".product-data").find(".prod_id").val();
    var product_qty = $(this).closest(".product-data").find(".qty-val").val();
    var token = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
      method: "POST",
      url: "/add-to-cart",
      data: {
        product_id: product_id,
        product_qty: product_qty,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        Toastify({
        text: response.status,
        duration: 3000
        }).showToast();
      },
    });
  });

  $(".changeQtyy").off('click').on('click', function (e) {
    e.preventDefault();

    var product_id = $(this).closest(".product-data").find(".prod_id").val();
    var product_qty = $(this).closest(".product-data").find(".qty-val").val();
    console.log(product_qty)
    var token = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
      method: "POST",
      url: "/update-cart",
      data: {
        product_id: product_id,
        product_qty: product_qty,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        Toastify({
        text: response.status,
        duration: 5000
        }).showToast();
      },
    });
  });

    $(".delete-cart-itemm").off('click').on("click", function (e) {
    e.preventDefault();

    var product_id = $(this).closest(".product-data").find(".prod_id").val();
    var token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      method: "POST",
      url: "/delete-cart-item",
      data: {
        product_id: product_id,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        Toastify({
        text: response.status,
        duration: 5000
        }).showToast();
        $(".cart_data").load(location.href + " .cart_data");
      },
    });
  });
});
