import axios from 'axios';
import React, { useEffect, useState } from 'react';
import type { FC } from "react";
import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import MainPost from '../parts/MainFeaturedPost';
import FeaturedPost from '../parts/FeaturedPost';

interface HwProps {
    csrfToken: string; // Add csrfToken to the props interface
}

const mainFeaturedPost = {
    title: 'ПАО «Газпром Нефть»',
    description:
        "Сервис для автоматического анализа текста требований и характеристик.",
    image: 'https://s.ura.news/images/news/upload/story/401/331005_Vistavka_Rossiya_ustreml_nnaya_v_budushtee_v_Manezhe_Moskva_gazprom_gazpromnefty_rosnefty_1300x360_4928.1363.0.1446.jpg',
    imageText: 'main image description',
};

const featuredPosts = [
    {
        title: 'Загрузите:',
        description:
            'требования компании в формате .doc/.docx',
    },
    {
        title: 'Загрузите:',
        description:
            'технические характеристики оборудования в формате .doc/.docx',
    },
];

const defaultTheme = createTheme();

const HwFunctionalComponent: FC<HwProps> = ({ csrfToken }) => {
    const [count, setCount] = useState(0);
    const [docsCount, setDocsCount] = useState('');

    useEffect(() => {
        // Fetch user count from the API
        axios.get('/api/users').then((response) => {
            setDocsCount(response.data.count);
        });
    }, []); // Empty dependency array to run the effect only once

    // Define the function to handle file upload
    const handleFileUpload = async (file: File, name: string) => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('name', name);
        formData.append('csrfmiddlewaretoken', GN.csrf_token);
    
        try {
            const response = await axios.post('/api/docs', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            console.log(response.data);
        } catch (error) {
            console.error('Error uploading file: ', error);
        }
    };

    return (
        <ThemeProvider theme={defaultTheme}>
            <Container maxWidth="lg" className='bg'>
                <main>
                    <MainPost post={mainFeaturedPost} />
                    <Grid container spacing={4}>
                        {/* Render FeaturedPost component for each item in featuredPosts */}
                        {featuredPosts.map((post, index) => (
                            <FeaturedPost key={index} post={post} onFileUpload={handleFileUpload} />
                        ))}
                    </Grid>
                </main>
            </Container>
        </ThemeProvider>
    );
}

export default HwFunctionalComponent;
