ФОТО ТОВАРОВ
============
products/  — брендовые SVG-плейсхолдеры под каждый товар (генерируются gen_placeholders.py).

Когда появятся реальные фото:
  1) положите файл в assets/products/ (например ip16p-256.jpg)
  2) в index.html в массиве PRODUCTS пропишите путь в поле photo:
       photo: "assets/products/ip16p-256.jpg"
  Если photo оставить пустым "" — используется плейсхолдер assets/products/{id}.svg

Перегенерировать плейсхолдеры: python3 gen_placeholders.py
