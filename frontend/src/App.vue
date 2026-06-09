<script setup>
import { ref } from 'vue'
import axios from 'axios'

const selectedFile = ref(null)

const originalImage = ref(null)
const selectedImage = ref(null)
const filteredImage = ref(null)

const initialMatrix = ref([])
const resultMatrix = ref([])

const useColor = ref(false)
const cropMode = ref('crop')
const filter = ref('mean')

const x = ref(0)
const y = ref(0)

const loading = ref(false)
const message = ref('')
const error = ref('')

const handleFileChange = (event) => {
  selectedFile.value = event.target.files[0]
  message.value = ''
  error.value = ''

  if (selectedFile.value) {
    originalImage.value = URL.createObjectURL(selectedFile.value)
  }
}

const processImage = async () => {
  if (!selectedFile.value) {
    error.value = 'Primero debes seleccionar una imagen.'
    return
  }

  loading.value = true
  message.value = ''
  error.value = ''

  const formData = new FormData()
  formData.append('image', selectedFile.value)
  formData.append('use_color', useColor.value)
  formData.append('crop_mode', cropMode.value)
  formData.append('filter', filter.value)
  formData.append('x', x.value)
  formData.append('y', y.value)

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/process-image/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    message.value = response.data.message
    originalImage.value = response.data.original_image
    selectedImage.value = response.data.selected_image
    filteredImage.value = response.data.filtered_image
    initialMatrix.value = response.data.initial_matrix
    resultMatrix.value = response.data.result_matrix
  } catch (err) {
    error.value = err.response?.data?.error || 'Ocurrió un error al procesar la imagen.'
  } finally {
    loading.value = false
  }
}

const resetApp = () => {
  selectedFile.value = null
  originalImage.value = null
  selectedImage.value = null
  filteredImage.value = null

  initialMatrix.value = []
  resultMatrix.value = []

  useColor.value = false
  cropMode.value = 'crop'
  filter.value = 'mean'

  x.value = 0
  y.value = 0

  message.value = ''
  error.value = ''

  const input = document.getElementById('image-input')
  if (input) input.value = ''
}

const formatMatrixValue = (value) => {
  if (Array.isArray(value)) {
    return `[${value.join(',')}]`
  }

  return String(value).padStart(3, ' ')
}
</script>

<template>
  <main class="page">
    <div class="animated-background">
      <div class="blob blob-one"></div>
      <div class="blob blob-two"></div>
      <div class="blob blob-three"></div>
    </div>

    <div class="grid-overlay"></div>

    <div class="floating-icons">
      <span>🧠</span>
      <span>🖼️</span>
      <span>🔍</span>
      <span>⚙️</span>
      <span>📊</span>
    </div>

    <section class="hero">
      <div class="hero-content">
        <span class="badge">Procesamiento digital de imágenes</span>
        <h1>ScanFilter Web</h1>
        <p>
          Plataforma web para cargar imágenes, aplicar filtros digitales y visualizar su
          representación matricial usando Django, Vue, OpenCV y NumPy.
        </p>

        <div class="tech-stack">
          <span>Django</span>
          <span>Vue.js</span>
          <span>OpenCV</span>
          <span>NumPy</span>
        </div>

        <div class="hero-actions">
          <a href="#processor" class="hero-button primary-hero">Probar procesamiento</a>
          <a href="#filters" class="hero-button secondary-hero">Ver filtros</a>
        </div>
      </div>
    </section>

    <section class="about-grid">
      <article class="about-card large-card">
        <span class="section-badge">¿Qué es ScanFilter Web?</span>
        <h2>Una herramienta web para entender el filtrado digital de imágenes</h2>
        <p>
          ScanFilter Web permite cargar imágenes JPG/JPEG, trabajar con una región de
          15x15 píxeles o con la imagen completa, aplicar filtros digitales y visualizar
          la representación matricial de los píxeles antes y después del procesamiento.
        </p>
        <p>
          El sistema está pensado como una herramienta educativa para comprender cómo una
          imagen digital puede ser analizada y transformada mediante operaciones
          computacionales.
        </p>
      </article>

      <article class="about-card objective-card">
        <span class="section-badge">Objetivo</span>
        <h2>Procesar imágenes de forma visual e intuitiva</h2>
        <p>
          El objetivo principal es desarrollar una aplicación web que permita aplicar
          filtros como media, mediana, laplaciano y Sobel, mostrando tanto el resultado
          visual como la matriz numérica correspondiente.
        </p>
      </article>
    </section>

    <section id="filters" class="filters-section">
      <div class="section-title center-title">
        <h2>Filtros disponibles</h2>
        <p>
          Cada filtro cumple una función distinta dentro del procesamiento digital de imágenes.
        </p>
      </div>

      <div class="filters-grid">
        <article class="filter-card">
          <span class="filter-icon">🌫️</span>
          <h3>Filtro de media</h3>
          <p>
            Suaviza la imagen calculando el promedio de los píxeles vecinos. Es útil
            para reducir pequeñas variaciones de intensidad.
          </p>
        </article>

        <article class="filter-card">
          <span class="filter-icon">🧹</span>
          <h3>Filtro de mediana</h3>
          <p>
            Reduce ruido conservando mejor los bordes. Es especialmente útil para
            imágenes con ruido tipo sal y pimienta.
          </p>
        </article>

        <article class="filter-card">
          <span class="filter-icon">⚡</span>
          <h3>Filtro laplaciano</h3>
          <p>
            Resalta cambios bruscos de intensidad, permitiendo detectar bordes y detalles
            importantes dentro de la imagen.
          </p>
        </article>

        <article class="filter-card">
          <span class="filter-icon">📐</span>
          <h3>Filtro Sobel</h3>
          <p>
            Detecta bordes horizontales y verticales, ayudando a identificar contornos
            y formas dentro de la imagen.
          </p>
        </article>
      </div>
    </section>

    <section class="applications-section">
      <div class="section-title center-title">
        <h2>Aplicaciones prácticas</h2>
        <p>
          El filtrado digital de imágenes puede utilizarse en distintos campos de análisis visual.
        </p>
      </div>

      <div class="applications-grid">
        <article class="application-card">
          <h3>Medicina</h3>
          <p>
            Puede apoyar la mejora visual de imágenes médicas, resaltando detalles en
            radiografías, tomografías o imágenes clínicas.
          </p>
        </article>

        <article class="application-card">
          <h3>Visión artificial</h3>
          <p>
            Sirve como etapa previa para reconocimiento de objetos, segmentación y
            análisis automático de imágenes.
          </p>
        </article>

        <article class="application-card">
          <h3>Educación</h3>
          <p>
            Permite observar cómo cambian los valores de una matriz de píxeles al aplicar
            diferentes filtros digitales.
          </p>
        </article>
      </div>
    </section>

    <section class="summary-grid">
      <article class="summary-card">
        <span class="summary-icon">🖼️</span>
        <div>
          <h3>Modo actual</h3>
          <p>{{ cropMode === 'crop' ? 'Recorte 15x15' : 'Imagen completa' }}</p>
        </div>
      </article>

      <article class="summary-card">
        <span class="summary-icon">🎨</span>
        <div>
          <h3>Tipo de imagen</h3>
          <p>{{ useColor ? 'Color RGB' : 'Escala de grises' }}</p>
        </div>
      </article>

      <article class="summary-card">
        <span class="summary-icon">🧪</span>
        <div>
          <h3>Filtro seleccionado</h3>
          <p>
            {{
              filter === 'mean'
                ? 'Media'
                : filter === 'median'
                  ? 'Mediana'
                  : filter === 'laplacian'
                    ? 'Laplaciano'
                    : 'Sobel'
            }}
          </p>
        </div>
      </article>
    </section>

    <section class="system-status">
      <article class="status-card">
        <span class="status-dot active"></span>
        <div>
          <h3>Backend conectado</h3>
          <p>Django API lista para procesar imágenes</p>
        </div>
      </article>

      <article class="status-card">
        <span class="status-dot blue"></span>
        <div>
          <h3>Procesamiento matricial</h3>
          <p>Conversión de imagen a matriz de píxeles</p>
        </div>
      </article>

      <article class="status-card">
        <span class="status-dot purple"></span>
        <div>
          <h3>Filtros digitales</h3>
          <p>Media, mediana, laplaciano y Sobel</p>
        </div>
      </article>
    </section>

    <section id="processor" class="controls-card">
      <div class="section-title">
        <h2>Configuración del procesamiento</h2>
        <p>Selecciona la imagen, el modo de trabajo y el filtro que deseas aplicar.</p>
      </div>

      <div class="controls-grid">
        <div class="field file-field">
          <label>Imagen JPG/JPEG</label>

          <label class="custom-file-upload" for="image-input">
            <span class="upload-icon">📁</span>
            <span>{{ selectedFile ? selectedFile.name : 'Seleccionar imagen' }}</span>
          </label>

          <input
            id="image-input"
            class="hidden-file-input"
            type="file"
            accept=".jpg,.jpeg,image/jpeg"
            @change="handleFileChange"
          />
        </div>

        <div class="field">
          <label>Modo</label>
          <select v-model="cropMode">
            <option value="crop">Recorte 15x15</option>
            <option value="full">Imagen completa</option>
          </select>
        </div>

        <div v-if="cropMode === 'crop'" class="field">
          <label>Coordenada X</label>
          <input type="number" v-model="x" min="0" />
        </div>

        <div v-if="cropMode === 'crop'" class="field">
          <label>Coordenada Y</label>
          <input type="number" v-model="y" min="0" />
        </div>

        <div class="field">
          <label>Filtro</label>
          <select v-model="filter">
            <option value="mean">Media</option>
            <option value="median">Mediana</option>
            <option value="laplacian">Laplaciano</option>
            <option value="sobel">Sobel</option>
          </select>
        </div>

        <div class="check-field">
          <label>
            <input type="checkbox" v-model="useColor" />
            Procesar a color
          </label>
        </div>

        <div class="buttons">
          <button class="primary" @click="processImage" :disabled="loading">
            {{ loading ? 'Procesando...' : 'Aplicar filtro' }}
          </button>

          <button class="secondary" @click="resetApp">
            Reiniciar
          </button>
        </div>
      </div>

      <p v-if="message" class="message">{{ message }}</p>
      <p v-if="error" class="error">{{ error }}</p>
    </section>

    <section class="workflow-card">
      <h2>Flujo del sistema</h2>
      <div class="steps">
        <div class="step">
          <span>1</span>
          <p>Cargar imagen</p>
        </div>
        <div class="step">
          <span>2</span>
          <p>Elegir modo</p>
        </div>
        <div class="step">
          <span>3</span>
          <p>Aplicar filtro</p>
        </div>
        <div class="step">
          <span>4</span>
          <p>Visualizar matrices</p>
        </div>
      </div>
    </section>

    <section class="images-grid">
      <article class="image-card">
        <div class="card-header">
          <h2>Imagen original</h2>
          <span>Entrada</span>
        </div>

        <div v-if="originalImage" class="image-preview">
          <img :src="originalImage" alt="Imagen original" />
          <span class="scanner-line"></span>
        </div>

        <div v-else class="empty">Sin imagen</div>
      </article>

      <article class="image-card">
        <div class="card-header">
          <h2>{{ cropMode === 'crop' ? 'Recorte 15x15' : 'Imagen completa' }}</h2>
          <span>Selección</span>
        </div>

        <div v-if="selectedImage" class="image-preview">
          <img :src="selectedImage" alt="Imagen seleccionada" />
          <span class="scanner-line"></span>
        </div>

        <div v-else class="empty">Sin procesamiento</div>
      </article>

      <article class="image-card">
        <div class="card-header">
          <h2>Imagen filtrada</h2>
          <span>Resultado</span>
        </div>

        <div v-if="filteredImage" class="image-preview">
          <img :src="filteredImage" alt="Imagen filtrada" />
          <span class="scanner-line"></span>
        </div>

        <div v-else class="empty">Sin filtro aplicado</div>
      </article>
    </section>

    <section class="matrix-grid">
      <article class="matrix-card">
        <div class="card-header">
          <h2>Matriz inicial</h2>
          <span>Valores de píxel</span>
        </div>

        <pre v-if="initialMatrix.length"><span
          v-for="(row, rowIndex) in initialMatrix"
          :key="rowIndex"
        ><span
          v-for="(value, valueIndex) in row"
          :key="valueIndex"
        >{{ formatMatrixValue(value) }} </span>
</span></pre>

        <div v-else class="empty matrix-empty">Sin matriz</div>
      </article>

      <article class="matrix-card">
        <div class="card-header">
          <h2>Matriz resultante</h2>
          <span>Después del filtro</span>
        </div>

        <pre v-if="resultMatrix.length"><span
          v-for="(row, rowIndex) in resultMatrix"
          :key="rowIndex"
        ><span
          v-for="(value, valueIndex) in row"
          :key="valueIndex"
        >{{ formatMatrixValue(value) }} </span>
</span></pre>

        <div v-else class="empty matrix-empty">Sin matriz</div>
      </article>
    </section>

    <footer class="footer">
      <p>ScanFilter Web — Proyecto de procesamiento digital de imágenes</p>
      <span>Python · Django · Vue · OpenCV · NumPy</span>
    </footer>
  </main>
</template>

<style scoped>
html {
  scroll-behavior: smooth;
}

.page {
  width: 100%;
  min-height: 100vh;
  overflow-x: hidden;
  padding: 36px;
  background:
    linear-gradient(120deg, rgba(239, 246, 255, 0.95), rgba(245, 243, 255, 0.95)),
    radial-gradient(circle at 20% 20%, rgba(96, 165, 250, 0.28), transparent 30%),
    radial-gradient(circle at 80% 10%, rgba(167, 139, 250, 0.28), transparent 28%),
    radial-gradient(circle at 50% 90%, rgba(52, 211, 153, 0.18), transparent 28%);
  color: #111827;
}

.animated-background {
  position: fixed;
  inset: 0;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}

.blob {
  position: absolute;
  width: 360px;
  height: 360px;
  border-radius: 50%;
  filter: blur(90px);
  opacity: 0.45;
  animation: floatBlob 10s ease-in-out infinite alternate;
}

.blob-one {
  top: 40px;
  left: 80px;
  background: #60a5fa;
}

.blob-two {
  top: 180px;
  right: 100px;
  background: #a78bfa;
  animation-delay: 1.5s;
}

.blob-three {
  bottom: 80px;
  left: 45%;
  background: #34d399;
  animation-delay: 3s;
}

@keyframes floatBlob {
  from {
    transform: translateY(0) scale(1);
  }

  to {
    transform: translateY(40px) scale(1.15);
  }
}

.grid-overlay {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
  background-image:
    linear-gradient(rgba(37, 99, 235, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(37, 99, 235, 0.06) 1px, transparent 1px);
  background-size: 42px 42px;
  mask-image: linear-gradient(to bottom, black, transparent 85%);
  animation: gridMove 18s linear infinite;
}

@keyframes gridMove {
  from {
    background-position: 0 0;
  }

  to {
    background-position: 84px 84px;
  }
}

.floating-icons {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}

.floating-icons span {
  position: absolute;
  font-size: 28px;
  opacity: 0.16;
  animation: floatIcon 8s ease-in-out infinite alternate;
}

.floating-icons span:nth-child(1) {
  top: 18%;
  left: 8%;
}

.floating-icons span:nth-child(2) {
  top: 28%;
  right: 10%;
  animation-delay: 1s;
}

.floating-icons span:nth-child(3) {
  top: 58%;
  left: 5%;
  animation-delay: 2s;
}

.floating-icons span:nth-child(4) {
  bottom: 18%;
  right: 8%;
  animation-delay: 3s;
}

.floating-icons span:nth-child(5) {
  bottom: 12%;
  left: 48%;
  animation-delay: 4s;
}

@keyframes floatIcon {
  from {
    transform: translateY(0) rotate(0deg) scale(1);
  }

  to {
    transform: translateY(-28px) rotate(8deg) scale(1.15);
  }
}

.hero,
.summary-grid,
.about-grid,
.filters-section,
.applications-section,
.controls-card,
.workflow-card,
.images-grid,
.matrix-grid,
.footer,
.system-status {
  position: relative;
  z-index: 1;
}

.hero {
  max-width: 1100px;
  margin: 0 auto 26px;
  text-align: center;
}

.hero-content {
  padding: 28px;
  border-radius: 28px;
  animation: fadeUp 0.7s ease both;
}

.badge {
  display: inline-block;
  margin-bottom: 14px;
  padding: 9px 16px;
  border-radius: 999px;
  background: #dbeafe;
  color: #1d4ed8;
  font-weight: 800;
  font-size: 13px;
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.18);
  animation: pulseBadge 2.2s ease-in-out infinite;
}

.hero h1 {
  position: relative;
  display: inline-block;
  margin: 0;
  font-size: 48px;
  letter-spacing: -1.5px;
  background: linear-gradient(135deg, #111827, #2563eb, #7c3aed);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero h1::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: -10px;
  width: 0;
  height: 4px;
  border-radius: 999px;
  background: linear-gradient(90deg, #2563eb, #7c3aed, #06b6d4);
  transform: translateX(-50%);
  animation: titleLine 1.2s ease forwards;
}

@keyframes titleLine {
  to {
    width: 75%;
  }
}

.hero p {
  max-width: 780px;
  margin: 24px auto 0;
  color: #4b5563;
  line-height: 1.7;
}

.tech-stack {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 18px;
}

.tech-stack span {
  padding: 8px 13px;
  border-radius: 999px;
  background: white;
  color: #374151;
  font-size: 13px;
  font-weight: 800;
  box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
  transition:
    transform 0.18s ease,
    background 0.18s ease,
    color 0.18s ease;
}

.tech-stack span:hover {
  transform: translateY(-3px);
  background: #2563eb;
  color: white;
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: 14px;
  flex-wrap: wrap;
  margin-top: 24px;
}

.hero-button {
  padding: 13px 18px;
  border-radius: 999px;
  text-decoration: none;
  font-weight: 900;
  transition:
    transform 0.18s ease,
    box-shadow 0.18s ease,
    background 0.18s ease;
}

.primary-hero {
  color: white;
  background: linear-gradient(135deg, #2563eb, #7c3aed);
  box-shadow: 0 14px 30px rgba(37, 99, 235, 0.28);
}

.secondary-hero {
  color: #1d4ed8;
  background: white;
  box-shadow: 0 12px 26px rgba(15, 23, 42, 0.1);
}

.hero-button:hover {
  transform: translateY(-4px) scale(1.03);
}

.primary-hero:hover {
  box-shadow: 0 20px 38px rgba(124, 58, 237, 0.35);
}

@keyframes pulseBadge {
  0%,
  100% {
    transform: scale(1);
  }

  50% {
    transform: scale(1.04);
  }
}

.about-grid {
  max-width: 1100px;
  width: 100%;
  margin: 0 auto 24px;
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 18px;
}

.about-card {
  padding: 26px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.78);
  backdrop-filter: blur(18px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow:
    0 18px 45px rgba(15, 23, 42, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.7);
}

.about-card h2 {
  margin: 12px 0;
  font-size: 26px;
  line-height: 1.25;
}

.about-card p {
  margin: 10px 0 0;
  color: #4b5563;
  line-height: 1.7;
}

.section-badge {
  display: inline-block;
  padding: 8px 13px;
  border-radius: 999px;
  background: #eef2ff;
  color: #4338ca;
  font-size: 13px;
  font-weight: 900;
}

.filters-section,
.applications-section {
  max-width: 1100px;
  width: 100%;
  margin: 0 auto 24px;
  padding: 26px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.78);
  backdrop-filter: blur(18px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow:
    0 18px 45px rgba(15, 23, 42, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.7);
}

.center-title {
  text-align: center;
  margin-bottom: 22px;
}

.center-title h2 {
  margin: 0;
  font-size: 28px;
}

.center-title p {
  margin: 8px auto 0;
  max-width: 700px;
  color: #6b7280;
  line-height: 1.6;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.filter-card {
  position: relative;
  overflow: hidden;
  min-width: 0;
  padding: 20px;
  border-radius: 22px;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.filter-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.12), rgba(124, 58, 237, 0.1));
  opacity: 0;
  transition: opacity 0.2s ease;
}

.filter-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 14px 28px rgba(15, 23, 42, 0.12);
}

.filter-card:hover::before {
  opacity: 1;
}

.filter-icon {
  position: relative;
  z-index: 1;
  width: 46px;
  height: 46px;
  display: grid;
  place-items: center;
  margin-bottom: 12px;
  border-radius: 16px;
  background: #dbeafe;
  font-size: 23px;
}

.filter-card:nth-child(1) .filter-icon {
  background: #dbeafe;
}

.filter-card:nth-child(2) .filter-icon {
  background: #dcfce7;
}

.filter-card:nth-child(3) .filter-icon {
  background: #ffedd5;
}

.filter-card:nth-child(4) .filter-icon {
  background: #ede9fe;
}

.filter-card h3,
.filter-card p {
  position: relative;
  z-index: 1;
}

.filter-card h3 {
  margin: 0 0 8px;
  font-size: 18px;
}

.filter-card p {
  margin: 0;
  color: #4b5563;
  line-height: 1.6;
  font-size: 14px;
}

.applications-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.application-card {
  padding: 22px;
  border-radius: 22px;
  background: linear-gradient(135deg, #eff6ff, #f5f3ff);
  border: 1px solid #e0e7ff;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.application-card:hover {
  transform: translateY(-5px) scale(1.01);
  box-shadow: 0 18px 35px rgba(79, 70, 229, 0.18);
}

.application-card h3 {
  margin: 0 0 8px;
  font-size: 19px;
  color: #1f2937;
}

.application-card p {
  margin: 0;
  color: #4b5563;
  line-height: 1.6;
}

.summary-grid {
  max-width: 1100px;
  width: 100%;
  margin: 0 auto 22px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

.summary-card {
  min-width: 0;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px;
  border-radius: 22px;
  background: rgba(255, 255, 255, 0.82);
  backdrop-filter: blur(12px);
  box-shadow: 0 14px 35px rgba(15, 23, 42, 0.1);
}

.summary-icon {
  width: 48px;
  height: 48px;
  display: grid;
  place-items: center;
  flex-shrink: 0;
  border-radius: 16px;
  background: #eff6ff;
  font-size: 24px;
}

.summary-card h3 {
  margin: 0;
  font-size: 14px;
  color: #6b7280;
}

.summary-card p {
  margin: 4px 0 0;
  font-size: 18px;
  font-weight: 900;
}

.system-status {
  max-width: 1100px;
  width: 100%;
  margin: 0 auto 24px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

.status-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px;
  border-radius: 22px;
  background: rgba(17, 24, 39, 0.88);
  color: white;
  box-shadow: 0 18px 45px rgba(15, 23, 42, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.12);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.status-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 26px 55px rgba(15, 23, 42, 0.26);
}

.status-card h3 {
  margin: 0;
  font-size: 17px;
}

.status-card p {
  margin: 5px 0 0;
  color: #cbd5e1;
  font-size: 14px;
}

.status-dot {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  border-radius: 50%;
  background: #22c55e;
  box-shadow: 0 0 0 8px rgba(34, 197, 94, 0.15);
  animation: pulseDot 1.5s ease-in-out infinite;
}

.status-dot.blue {
  background: #38bdf8;
  box-shadow: 0 0 0 8px rgba(56, 189, 248, 0.15);
}

.status-dot.purple {
  background: #a78bfa;
  box-shadow: 0 0 0 8px rgba(167, 139, 250, 0.15);
}

@keyframes pulseDot {
  0%,
  100% {
    transform: scale(1);
    opacity: 1;
  }

  50% {
    transform: scale(1.25);
    opacity: 0.7;
  }
}

.controls-card,
.workflow-card,
.image-card,
.matrix-card {
  background: rgba(255, 255, 255, 0.78);
  backdrop-filter: blur(18px);
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow:
    0 18px 45px rgba(15, 23, 42, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.7);
}

.summary-card,
.about-card,
.filter-card,
.application-card,
.controls-card,
.workflow-card,
.image-card,
.matrix-card,
.status-card {
  animation: fadeUp 0.8s ease both;
  transform-style: preserve-3d;
}

.summary-card,
.about-card,
.controls-card,
.workflow-card,
.image-card,
.matrix-card,
.filters-section,
.applications-section {
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    border-color 0.2s ease;
}

.summary-card:hover,
.about-card:hover,
.filter-card:hover,
.application-card:hover,
.controls-card:hover,
.workflow-card:hover,
.image-card:hover,
.matrix-card:hover {
  transform: perspective(900px) rotateX(1.2deg) rotateY(-1.2deg) translateY(-6px);
}

.summary-card:hover,
.about-card:hover,
.controls-card:hover,
.workflow-card:hover,
.image-card:hover,
.matrix-card:hover,
.filters-section:hover,
.applications-section:hover {
  box-shadow: 0 24px 55px rgba(15, 23, 42, 0.16);
  border-color: rgba(37, 99, 235, 0.25);
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(24px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.controls-card {
  max-width: 1100px;
  width: 100%;
  margin: 0 auto 24px;
  padding: 26px;
  border-radius: 28px;
}

.controls-card,
.filters-section,
.applications-section,
.workflow-card {
  position: relative;
  overflow: hidden;
}

.controls-card::before,
.filters-section::before,
.applications-section::before,
.workflow-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    120deg,
    transparent,
    rgba(37, 99, 235, 0.08),
    transparent
  );
  transform: translateX(-120%);
  transition: transform 0.7s ease;
}

.controls-card:hover::before,
.filters-section:hover::before,
.applications-section:hover::before,
.workflow-card:hover::before {
  transform: translateX(120%);
}

.controls-card > *,
.filters-section > *,
.applications-section > *,
.workflow-card > * {
  position: relative;
  z-index: 1;
}

.section-title {
  margin-bottom: 20px;
}

.section-title h2 {
  margin: 0;
  font-size: 24px;
}

.section-title p {
  margin: 6px 0 0;
  color: #6b7280;
}

.controls-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 18px;
  align-items: end;
}

.field,
.check-field {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.field label {
  font-size: 14px;
  font-weight: 900;
  color: #374151;
}

.field input,
.field select {
  width: 100%;
  padding: 13px 14px;
  border: 1px solid #d1d5db;
  border-radius: 15px;
  background: #f9fafb;
  color: #111827;
  outline: none;
}

.field input:focus,
.field select:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.14);
}

.file-field {
  grid-column: span 2;
}

.hidden-file-input {
  display: none;
}

.custom-file-upload {
  width: 100%;
  min-height: 48px;
  padding: 13px 14px;
  border: 1px dashed #93c5fd;
  border-radius: 15px;
  background: linear-gradient(135deg, #eff6ff, #eef2ff);
  color: #1d4ed8;
  font-weight: 900;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 10px;
  transition:
    transform 0.15s ease,
    background 0.15s ease,
    border-color 0.15s ease,
    box-shadow 0.15s ease;
}

.custom-file-upload:hover {
  background: linear-gradient(135deg, #dbeafe, #ede9fe);
  border-color: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 10px 22px rgba(37, 99, 235, 0.18);
}

.upload-icon {
  font-size: 20px;
}

.check-field {
  justify-content: center;
}

.check-field label {
  display: flex;
  align-items: center;
  gap: 9px;
  font-weight: 900;
  color: #374151;
}

.buttons {
  display: flex;
  gap: 10px;
}

button {
  width: 100%;
  min-height: 54px;
  padding: 13px 16px;
  border: none;
  border-radius: 16px;
  color: white;
  font-weight: 900;
  cursor: pointer;
  transition:
    transform 0.15s ease,
    opacity 0.15s ease,
    box-shadow 0.15s ease;
}

button:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 24px rgba(37, 99, 235, 0.25);
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.primary {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #2563eb, #4f46e5);
}

.primary::after {
  content: '';
  position: absolute;
  top: 0;
  left: -120%;
  width: 80%;
  height: 100%;
  background: linear-gradient(
    120deg,
    transparent,
    rgba(255, 255, 255, 0.35),
    transparent
  );
  transition: left 0.45s ease;
}

.primary:hover::after {
  left: 120%;
}

.secondary {
  background: linear-gradient(135deg, #6b7280, #374151);
}

.message,
.error {
  margin: 18px 0 0;
  padding: 14px 16px;
  border-radius: 16px;
  font-weight: 900;
}

.message {
  background: #dcfce7;
  color: #166534;
}

.error {
  background: #fee2e2;
  color: #991b1b;
}

.workflow-card {
  max-width: 1100px;
  width: 100%;
  margin: 0 auto 24px;
  padding: 24px;
  border-radius: 28px;
}

.workflow-card h2 {
  margin: 0 0 18px;
}

.steps {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.step {
  position: relative;
  overflow: hidden;
  min-width: 0;
  padding: 16px;
  border-radius: 18px;
  background: #f8fafc;
  text-align: center;
  transition:
    transform 0.18s ease,
    background 0.18s ease,
    box-shadow 0.18s ease;
}

.step::after {
  content: '';
  position: absolute;
  inset: auto -20% -60% -20%;
  height: 80px;
  background: rgba(37, 99, 235, 0.12);
  transform: rotate(-8deg);
  transition: bottom 0.25s ease;
}

.step:hover {
  transform: translateY(-4px);
  background: white;
  box-shadow: 0 14px 28px rgba(15, 23, 42, 0.1);
}

.step:hover::after {
  bottom: -35%;
}

.step span {
  width: 36px;
  height: 36px;
  display: grid;
  place-items: center;
  margin: 0 auto 10px;
  border-radius: 50%;
  background: #2563eb;
  color: white;
  font-weight: 900;
}

.step span,
.step p {
  position: relative;
  z-index: 1;
}

.step p {
  margin: 0;
  font-weight: 800;
  color: #374151;
}

.images-grid {
  max-width: 1100px;
  width: 100%;
  margin: 0 auto 24px;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
}

.image-card,
.matrix-card {
  min-width: 0;
  padding: 20px;
  border-radius: 28px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
  margin-bottom: 14px;
}

.card-header h2 {
  margin: 0;
  font-size: 19px;
}

.card-header span {
  padding: 6px 10px;
  border-radius: 999px;
  background: #eef2ff;
  color: #4338ca;
  font-size: 12px;
  font-weight: 900;
  white-space: nowrap;
  transition:
    background 0.2s ease,
    color 0.2s ease,
    transform 0.2s ease;
}

.image-card:hover .card-header span,
.matrix-card:hover .card-header span {
  background: #2563eb;
  color: white;
  transform: translateY(-1px);
}

.image-preview {
  position: relative;
  width: 100%;
  height: 265px;
  overflow: hidden;
  border-radius: 18px;
  background:
    linear-gradient(45deg, #e5e7eb 25%, transparent 25%),
    linear-gradient(-45deg, #e5e7eb 25%, transparent 25%),
    linear-gradient(45deg, transparent 75%, #e5e7eb 75%),
    linear-gradient(-45deg, transparent 75%, #e5e7eb 75%);
  background-size: 22px 22px;
  background-position: 0 0, 0 11px, 11px -11px, -11px 0;
}

.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition:
    transform 0.25s ease,
    filter 0.25s ease;
}

.image-card:hover img {
  transform: scale(1.03);
  filter: saturate(1.12) contrast(1.05);
}

.scanner-line {
  position: absolute;
  left: 0;
  top: -20%;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, transparent, #38bdf8, #a78bfa, transparent);
  box-shadow: 0 0 18px rgba(56, 189, 248, 0.9);
  animation: scanImage 2.8s ease-in-out infinite;
  opacity: 0;
}

.image-preview:hover .scanner-line {
  opacity: 1;
}

@keyframes scanImage {
  0% {
    top: -10%;
  }

  50% {
    top: 105%;
  }

  100% {
    top: -10%;
  }
}

.empty {
  height: 265px;
  display: grid;
  place-items: center;
  background: #e5e7eb;
  border-radius: 18px;
  color: #6b7280;
  font-weight: 900;
  text-align: center;
}

.matrix-grid {
  max-width: 1100px;
  width: 100%;
  margin: 0 auto 26px;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 18px;
  overflow: hidden;
}

pre {
  position: relative;
  width: 100%;
  max-width: 100%;
  height: 320px;
  margin: 0;
  overflow: auto;
  padding: 18px;
  background: linear-gradient(135deg, #111827, #1f2937);
  color: #e5e7eb;
  border-radius: 18px;
  font-size: 13px;
  line-height: 1.65;
  white-space: pre;
  border: 1px solid rgba(147, 197, 253, 0.18);
  box-shadow: inset 0 0 28px rgba(37, 99, 235, 0.08);
}

pre::selection {
  background: #38bdf8;
  color: #111827;
}

.matrix-empty {
  height: 320px;
}

.footer {
  max-width: 1100px;
  width: 100%;
  margin: 0 auto;
  padding: 22px;
  text-align: center;
  color: #6b7280;
  position: relative;
}

.footer::before {
  content: '';
  display: block;
  width: 120px;
  height: 4px;
  margin: 0 auto 18px;
  border-radius: 999px;
  background: linear-gradient(90deg, #2563eb, #7c3aed, #06b6d4);
}

.footer p {
  margin: 0 0 6px;
  font-weight: 900;
  color: #374151;
}

.footer span {
  font-size: 14px;
}

@media (max-width: 950px) {
  .summary-grid,
  .about-grid,
  .filters-grid,
  .applications-grid,
  .controls-grid,
  .steps,
  .images-grid,
  .matrix-grid,
  .system-status {
    grid-template-columns: 1fr;
  }

  .file-field {
    grid-column: span 1;
  }

  .hero h1 {
    font-size: 36px;
  }

  .page {
    padding: 22px;
  }

  .buttons {
    flex-direction: column;
  }

  .hero-actions {
    flex-direction: column;
    align-items: center;
  }

  .hero-button {
    width: 100%;
    max-width: 280px;
    text-align: center;
  }
}
</style>
