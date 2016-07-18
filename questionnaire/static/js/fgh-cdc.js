$(document).ready(function() {
    $('#sidebar-toggle').click(function(e) {
        e.preventDefault();
            $('#left-content').toggle();
            //$("i", this).toggleClass("icon-circle-arrow-up icon-circle-arrow-down");
            $("div", this).toggleClass("SidebarOpen SidebarClose")
       });

});


