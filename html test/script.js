const photoFrame = document.getElementById('photo-frame');
const imageDirectory = 'C:/Users/schol/OneDrive/Documenten/GitHub/Scholtepa/html test/data/';

const images = [
    'Epson_11102019163131.jpg',
    'pasfoto Anne.jpg',
    'rene.jpg',
    // Add all image filenames here
];

images.forEach(image => {
    const imgElement = document.createElement('img');
    imgElement.src = `${imageDirectory}${image}`;
    photoFrame.appendChild(imgElement);
});