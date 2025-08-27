import { Camera, CameraResultType, CameraSource } from '@capacitor/camera';
import { PushNotifications } from '@capacitor/push-notifications';
import { Device } from '@capacitor/device';
import { App } from '@capacitor/app';
import { NativeBiometric } from 'capacitor-native-biometric';

export const takePicture = async () => {
  const image = await Camera.getPhoto({
    quality: 90,
    allowEditing: true,
    resultType: CameraResultType.Uri,
    source: CameraSource.Camera,
  });

  return image.webPath;
};

export const addPushNotificationsListeners = async () => {
  await PushNotifications.requestPermissions();
  await PushNotifications.register();

  PushNotifications.addListener('registration', (token) => {
    console.info('Registration token: ', token.value);
  });

  PushNotifications.addListener('registrationError', (err) => {
    console.error('Registration error: ', err.error);
  });

  PushNotifications.addListener('pushNotificationReceived', (notification) => {
    console.log('Push notification received: ', notification);
  });

  PushNotifications.addListener('pushNotificationActionPerformed', (notification) => {
    console.log('Push notification action performed', notification.actionId, notification.inputValue);
  });
};

export const getDeviceInfo = async () => {
  const info = await Device.getInfo();
  return info;
};

export const addBiometricAuth = async () => {
  const result = await NativeBiometric.isAvailable();
  if (!result.isAvailable) {
    console.log('Biometric authentication not available.');
    return;
  }

  const verified = await NativeBiometric.verifyIdentity({
    reason: 'For easy authentication',
    title: 'Authenticate',
    subtitle: 'Please use your biometrics to continue',
    description: 'Authenticate with your biometrics to access the app',
  })
    .then(() => true)
    .catch(() => false);

  if (verified) {
    console.log('Biometric authentication successful.');
  } else {
    console.log('Biometric authentication failed.');
  }
};

App.addListener('appStateChange', ({ isActive }) => {
  console.log('App state changed. Is active?', isActive);
});

App.addListener('appUrlOpen', (data) => {
  console.log('App opened with URL: ', data);
});

App.addListener('appRestoredResult', (data) => {
  console.log('Restored state:', data);
});