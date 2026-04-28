-- Nettoyage des données existantes pour éviter les doublons
DELETE FROM increments;
DELETE FROM items;
DELETE FROM lists;

-- 1. Insertion des Listes avec noms distincts
INSERT INTO lists (id, name) VALUES (1, 'latkhoussa 1');
INSERT INTO lists (id, name) VALUES (2, 'latkhoussa 2');
INSERT INTO lists (id, name) VALUES (3, 'latkhoussa 3');

-- 2. Items pour latkhoussa 1
INSERT INTO items (name, list_id, order_index) VALUES 
('Déodorant', 1, 0), 
('Concealer 1', 1, 1), 
('Concealer 2', 1, 2), 
('Parfum', 1, 3), 
('Écran solaire', 1, 4), 
('Pallette', 1, 5), 
('Rouge à lèvres', 1, 6), 
('Base', 1, 7), 
('Blush', 1, 8), 
('Highlighter', 1, 9), 
('Lip liner', 1, 10), 
('Chita 1', 1, 11), 
('Chita 2', 1, 12), 
('Mebred', 1, 13), 
('Mechta', 1, 14);

-- 3. Items pour latkhoussa 2
INSERT INTO items (name, list_id, order_index) VALUES 
('Démaquillant', 2, 0), 
('Fixateur', 2, 1), 
('Huile cheuveux', 2, 2), 
('Bronzer', 2, 3), 
('Chita 1', 2, 4), 
('Chita 1', 2, 5), 
('7ejbaniteur', 2, 6), 
('Anti taches', 2, 7), 
('Blush', 2, 8), 
('Powder', 2, 9), 
('Mechta', 2, 10);

-- 4. Items pour latkhoussa 3
INSERT INTO items (name, list_id, order_index) VALUES 
('Démêlant', 3, 0), 
('Crème corps', 3, 1), 
('Huile corps', 3, 2), 
('Scrub', 3, 3), 
('Crème cheuveux', 3, 4), 
('Nettoyeur visage', 3, 5), 
('Fix cheuveux', 3, 6);