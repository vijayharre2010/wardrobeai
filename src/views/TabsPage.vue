<template>
  <ion-page>
    <ion-tabs>
      <ion-router-outlet></ion-router-outlet>
      <ion-tab-bar slot="bottom">
        <ion-tab-button tab="tab1" href="/home/suggestions">
          <ion-icon aria-hidden="true" :icon="calendar" />
          <ion-label>Daily</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="tab2" href="/home/generate">
          <ion-icon aria-hidden="true" :icon="sparkles" />
          <ion-label>Generate</ion-label>
        </ion-tab-button>

        <ion-tab-button tab="tab3" href="/home/settings">
          <ion-icon aria-hidden="true" :icon="settings" />
          <ion-label>Settings</ion-label>
        </ion-tab-button>
      </ion-tab-bar>
    </ion-tabs>
  </ion-page>
</template>

<script setup lang="ts">
import { IonTabBar, IonTabButton, IonTabs, IonLabel, IonIcon, IonPage, IonRouterOutlet } from '@ionic/vue';
import { calendar, ellipse, settings, sparkles, square, triangle } from 'ionicons/icons';
</script>
