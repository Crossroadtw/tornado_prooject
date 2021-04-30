(function () {
    var avatar_img = document.querySelector("#avatar-img")
    var menu = document.querySelector(".menu")


    avatar_img.addEventListener('click', function () {
        var opacity = menu.style.opacity
        if (opacity == 1) {
            menu.style.opacity = 0
        } else {
            menu.style.opacity = 1
        }
    })

    avatar_img.addEventListener('dblclick',function () {

        window.location.href='/'

    })

}())
