function update_markdown() {
    var xhr = new XMLHttpRequest();
    xhr.open("PUT", '/post_article/', true);
    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    xhr.onload = function () {
        var res = JSON.parse(xhr.responseText);
        if (xhr.readyState == 4 && xhr.status == "200") {
            document.querySelector("#html-markdown").innerHTML = res.html
            console.table(res);
        } else {
            console.error(res);
        }
    }
    data = {}
    data.text = document.querySelector("#markdown").value
    console.log(data)
    json = JSON.stringify(data)
    xhr.send(json);
}

function delete_post(e) {

    var id = e.dataset.id
    var xhr = new XMLHttpRequest();
    xhr.open('DELETE', '/manage_article', true)
    xhr.setRequestHeader('Content-type', 'application/json;charset=utf-8')
    xhr.onload = function () {
        if (xhr.readyState == 4 && xhr.status == "200") {
            window.location.href = "/manage_article"
        } else {
            console.error('删除失败')
        }

    }
    var data = {}
    data.id = id
    console.log(data)
    var json = JSON.stringify(data)
    xhr.send(json);

}
