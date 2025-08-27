import {
  IonContent,
  IonHeader,
  IonPage,
  IonTitle,
  IonToolbar,
  IonButton,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardContent,
  IonItem,
  IonLabel,
  IonInput,
  IonLoading,
} from '@ionic/react';
import './Home.css';
import { useState, useEffect } from 'react';
import { generateOutfit, generateOutfitImage } from '../services/apiService';
import { useAppwrite } from '../services/appwriteService';
import {
  takePicture,
  addPushNotificationsListeners,
  getDeviceInfo,
  addBiometricAuth,
} from '../services/nativeService';

const Home: React.FC = () => {
  const [userDetails, setUserDetails] = useState({
    gender: '',
    age: '',
    bodyType: '',
    height: '',
    weight: '',
    skinTone: '',
    hairColor: '',
    eyeColor: '',
    stylePreferences: '',
    season: '',
  });

  const [outfit, setOutfit] = useState<any>(null);
  const [imageUrl, setImageUrl] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const { createAnonymousSession, isAuthenticated } = useAppwrite();
  const [authenticated, setAuthenticated] = useState(false);
  const [profilePic, setProfilePic] = useState<string | undefined>('');

  useEffect(() => {
    const checkAuth = async () => {
      const auth = await isAuthenticated();
      setAuthenticated(auth);

      if (!auth) {
        try {
          await createAnonymousSession();
          const verified = await isAuthenticated();
          setAuthenticated(verified);
        } catch (error) {
          console.error('Error creating session:', error);
        }
      }
    };

    checkAuth();
  }, []);

  useEffect(() => {
    addPushNotificationsListeners();
    getDeviceInfo().then((info) => console.log(info));
  }, []);

  const handleTakePicture = async () => {
    const picture = await takePicture();
    setProfilePic(picture);
  };

  const handleInputChange = (e: any) => {
    const { name, value } = e.target;
    setUserDetails({
      ...userDetails,
      [name]: value,
    });
  };

  const handleGenerateOutfit = async () => {
    setLoading(true);
    try {
      // Generate outfit text
      const outfitData = await generateOutfit(userDetails);
      setOutfit(outfitData);

      // Generate outfit image based on description
      if (outfitData && outfitData.outfit) {
        const description = outfitData.outfit
          .map((item: any) => item.description)
          .join(', ');
        const imageUrl = await generateOutfitImage(
          `Fashion model wearing: ${description}`
        );
        setImageUrl(imageUrl);
      }
    } catch (error) {
      console.error('Error generating outfit:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>WardrobeAI</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <IonHeader collapse="condense">
          <IonToolbar>
            <IonTitle size="large">WardrobeAI</IonTitle>
          </IonToolbar>
        </IonHeader>

        {!authenticated ? (
          <IonCard>
            <IonCardHeader>
              <IonCardTitle>Loading...</IonCardTitle>
            </IonCardHeader>
            <IonCardContent>
              <p>Authenticating...</p>
            </IonCardContent>
          </IonCard>
        ) : (
          <IonCard>
            <IonCardHeader>
              <IonCardTitle>Generate Your Outfit</IonCardTitle>
            </IonCardHeader>
            <IonCardContent>
              <IonButton expand="block" onClick={handleTakePicture}>
                Take Profile Picture
              </IonButton>
              {profilePic && (
                <img
                  src={profilePic}
                  alt="Profile"
                  style={{
                    width: '100px',
                    height: '100px',
                    borderRadius: '50%',
                    margin: '10px 0',
                  }}
                />
              )}
              <IonItem>
                <IonLabel position="stacked">Gender</IonLabel>
                <IonInput
                  name="gender"
                  value={userDetails.gender}
                  onIonChange={handleInputChange}
                />
              </IonItem>

              <IonItem>
                <IonLabel position="stacked">Age</IonLabel>
                <IonInput
                  name="age"
                  type="number"
                  value={userDetails.age}
                  onIonChange={handleInputChange}
                />
              </IonItem>

              <IonItem>
                <IonLabel position="stacked">Body Type</IonLabel>
                <IonInput
                  name="bodyType"
                  value={userDetails.bodyType}
                  onIonChange={handleInputChange}
                />
              </IonItem>

              <IonItem>
                <IonLabel position="stacked">Height</IonLabel>
                <IonInput
                  name="height"
                  value={userDetails.height}
                  onIonChange={handleInputChange}
                />
              </IonItem>

              <IonItem>
                <IonLabel position="stacked">Weight</IonLabel>
                <IonInput
                  name="weight"
                  value={userDetails.weight}
                  onIonChange={handleInputChange}
                />
              </IonItem>

              <IonItem>
                <IonLabel position="stacked">Skin Tone</IonLabel>
                <IonInput
                  name="skinTone"
                  value={userDetails.skinTone}
                  onIonChange={handleInputChange}
                />
              </IonItem>

              <IonItem>
                <IonLabel position="stacked">Hair Color</IonLabel>
                <IonInput
                  name="hairColor"
                  value={userDetails.hairColor}
                  onIonChange={handleInputChange}
                />
              </IonItem>

              <IonItem>
                <IonLabel position="stacked">Eye Color</IonLabel>
                <IonInput
                  name="eyeColor"
                  value={userDetails.eyeColor}
                  onIonChange={handleInputChange}
                />
              </IonItem>

              <IonItem>
                <IonLabel position="stacked">Style Preferences</IonLabel>
                <IonInput
                  name="stylePreferences"
                  value={userDetails.stylePreferences}
                  onIonChange={handleInputChange}
                />
              </IonItem>

              <IonItem>
                <IonLabel position="stacked">Season</IonLabel>
                <IonInput
                  name="season"
                  value={userDetails.season}
                  onIonChange={handleInputChange}
                />
              </IonItem>

              <IonButton
                expand="block"
                onClick={handleGenerateOutfit}
                disabled={loading}
              >
                Generate Outfit
              </IonButton>
              <IonButton
                expand="block"
                onClick={addBiometricAuth}
                style={{ marginTop: '10px' }}
              >
                Enable Biometric Auth
              </IonButton>
            </IonCardContent>
          </IonCard>
        )}

        {loading && (
          <IonLoading isOpen={loading} message="Generating your outfit..." />
        )}

        {outfit && (
          <IonCard>
            <IonCardHeader>
              <IonCardTitle>Your Outfit</IonCardTitle>
            </IonCardHeader>
            <IonCardContent>
              {imageUrl && (
                <img
                  src={imageUrl}
                  alt="Generated outfit"
                  style={{ width: '100%', marginBottom: '10px' }}
                />
              )}
              <pre>{JSON.stringify(outfit, null, 2)}</pre>
            </IonCardContent>
          </IonCard>
        )}
      </IonContent>
    </IonPage>
  );
};

export default Home;
