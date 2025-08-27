<template>
  <ion-page>
    <ion-content>
      <!-- Card Container for Side-by-Side Layout -->
      <div class="card-container">
        <ion-card class="custom-card" v-for="card in cards" :key="card.id">
          <img :alt="card.title" :src="card.img" />
          <ion-card-header>
            <ion-card-title>{{ card.title }}</ion-card-title>
            <ion-card-subtitle>{{ card.subtitle }}</ion-card-subtitle>
          </ion-card-header>
          <ion-card-content>
            {{ card.content }}
          </ion-card-content>
        </ion-card>
      </div>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { onIonViewWillEnter, IonPage, IonCard, IonCardContent, IonCardHeader, IonCardSubtitle, IonCardTitle, IonContent } from '@ionic/vue';

export default defineComponent({
  components: { IonPage, IonCard, IonCardContent, IonCardHeader, IonCardSubtitle, IonCardTitle, IonContent },
  setup() {
    const cards = ref<Array<{ id: number; title: string; subtitle: string; content: string; img: string }>>([]);

    // Function to populate or refresh cards
    const loadCards = () => {
      cards.value = [
        {
          id: 1,
          title: 'Card Title 1',
          subtitle: 'Card Subtitle',
          content: "Here's a small text description for the card content. Nothing more, nothing less.",
          img: 'https://wallpapers.com/images/hd/1920x1080-aesthetic-glrfk0ntspz3tvxg.jpg'
        },
        {
          id: 2,
          title: 'Card Title 2',
          subtitle: 'Card Subtitle',
          content: "Here's a small text description for the card content. Nothing more, nothing less.",
          img: 'https://wallpapers.com/images/hd/1920x1080-aesthetic-glrfk0ntspz3tvxg.jpg'
        },
        {
          id: 3,
          title: 'Card Title 3',
          subtitle: 'Card Subtitle',
          content: "Here's a small text description for the card content. Nothing more, nothing less.",
          img: 'https://wallpapers.com/images/hd/1920x1080-aesthetic-glrfk0ntspz3tvxg.jpg'
        }
      ];
    };

    // Refresh cards every time Tab1 becomes active
    onIonViewWillEnter(() => {
      loadCards();
    });

    // Initial load
    loadCards();

    return { cards };
  }
});
</script>

<style scoped>
.card-container {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  padding: 50px;
}

.custom-card {
  flex: 1;
  margin: 8px;
  min-width: 250px;
  max-width: 350px;
  background-color: var(--ion-color-dark);
  min-height: 650px;
}

/* Responsive design: Stack cards vertically on smaller screens */
@media (max-width: 768px) {
  .card-container {
    flex-direction: column;
    align-items: center;
  }
  .custom-card {
    width: 100%;
    max-width: 100%;
  }
}
</style>
