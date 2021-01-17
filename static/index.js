function onClick(id_pos, id_neg) {
    let pos = document.getElementById(id_pos);
    let neg = document.getElementById(id_neg);

    if (pos.className === 'btn btn-outline-success') {
        pos.className = 'btn btn-success';
    } else {
        pos.className = 'btn btn-outline-success';
    }
    if (neg.className === 'btn btn-success') {
        neg.className = 'btn btn-outline-success';
    }
}