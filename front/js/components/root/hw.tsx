import axios from 'axios';
import React, { useEffect, useState } from 'react';
import type { FC } from "react";
import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import MainPost from './MainFeaturedPost';
import FeaturedPost from './FeaturedPost';

interface HwProps {
}

const mainFeaturedPost = {
    title: 'ПАО «Газпром Нефть»',
    description:
        "Сервис для автоматического анализа текста требований и характеристик.",
    image: 'https://source.unsplash.com/random?wallpapers',
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

const HwFunctionalComponent: FC<HwProps> = ({ }) => {
    const [count, setCount] = useState(0);
    const [docsCount, setDocsCount] = useState('');

    useEffect(() => {
        // todo refactor hardcoded url
        axios.get('/api/users').then((response) => {
            setDocsCount(response.data.count);
        });
    });

    return (
        <>
            <ThemeProvider theme={defaultTheme}>

                <Container maxWidth="lg">
                    <main>
                        <MainPost post={mainFeaturedPost} />
                        <Grid container spacing={4}>
                            {featuredPosts.map((post) => (
                                <FeaturedPost key={post.title} post={post} />
                            ))}
                        </Grid>
                    </main>
                </Container>
            </ThemeProvider>
        </>
    );
}

export default HwFunctionalComponent;
