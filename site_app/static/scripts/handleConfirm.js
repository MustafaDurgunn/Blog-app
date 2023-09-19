const get_approval = (event, id) => {
    // a'nın varsayılan değerlerini sil
    event.preventDefault()

    const onayla = window.confirm("Bu tweeti cidden silmek istiyor musunuz?")

    if (onayla) {

        window.location = `http://127.0.0.1:8000/tweets/${id}/delete`
    }

}