function toggleOptions(option) {
    document.getElementById('price_field').style.display = 'none';
    document.getElementById('percentage_field').style.display = 'none';
    document.getElementById('price_to_field').style.display = 'none';

    if (option === 'price') {
        document.getElementById('price_field').style.display = 'block';
    } else if (option === 'percentage') {
        document.getElementById('percentage_field').style.display = 'block';
    } else if (option === 'price_to') {
        document.getElementById('price_to_field').style.display = 'block';
    }
}
